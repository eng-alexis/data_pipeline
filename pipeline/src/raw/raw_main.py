    # Importa funções

from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_exec import reg_new_execution, update_execution
from pipeline.common.monitoring.pipeline_step import reg_new_step
from pipeline.common.context.pipeline_context import upd_watermark_exec

from pipeline.src.raw.validate.schema_validate import schema_event_validation, schema_product_validation, schema_store_validation

from pipeline.src.raw.extract.extract_json import extrair_registros
from pipeline.src.raw.file_control.search_file_hist import gerar_hash, find_hash
from pipeline.src.raw.file_control.move_files import reg_novo_arquivo, move_file
from pipeline.src.raw.load.load_raw import load_to_raw, load_to_quarentine, descobrir_entidade

from pipeline.config.paths import JSON_PROCESSED_DIR, JSON_DUPLICATE_DIR

from pathlib import Path
from datetime import datetime

path_processado = JSON_PROCESSED_DIR
path_duplicado  = JSON_DUPLICATE_DIR

    # Diretorios e utilitarios

conexao_bd = get_db_connection()

def etapa_raw(id_execution, json_file):
  
    try:

    # Inicia Pipeline

        id_exec = id_execution
        arquivo = json_file
        inicio_pipeline = datetime.now()

    # extrai informações 

        hash_arquivo    = gerar_hash(arquivo)
        nome_arquivo    = Path(arquivo).name
        tamanho_bytes   = arquivo.stat().st_size

    # Registra nova execução do pipeline na tabela de auditoria

        new_exec = reg_new_execution(conexao_bd, id_exec, inicio_pipeline, nome_arquivo, hash_arquivo)
        conexao_bd.commit()

    # Valida arquivo

        sh_file  = find_hash(conexao_bd, hash_arquivo)
        
    # Aualiza tabela de auditoria, caso hash já exista no banco

        if sh_file:

            fim = datetime.now()

            upd_exec    = update_execution(conexao_bd, id_exec, fim, "DUPLICADO", "Hash já processado anteriormente")
            upd_id_exec = upd_watermark_exec(conexao_bd, id_exec, fim)
            conexao_bd.commit()


    # Move arquivo duplicado para pasta arq_duplicados

            move_file(arquivo, path_duplicado)

    # Registra novo arquivo na tabela de auditoria.

        else:

            data_ingestao = datetime.now()
            
            new_file = reg_novo_arquivo(conexao_bd, hash_arquivo, nome_arquivo, data_ingestao, tamanho_bytes, id_exec)
            conexao_bd.commit()

            if new_file:
               
                
    # Descobre a entidade

                entidade = descobrir_entidade(arquivo)
                print("checkpoint 01")

                TABELAS_RAW = {"eventos","produtos","lojas"}

                if entidade not in TABELAS_RAW:
                    raise ValueError(f"Entidade inválida: {entidade}")

    # Extrai registros e cria Lote.
                
                if entidade == "eventos":
                    tipo_file = "jsonl"

                else:
                    tipo_file = "json"

                registros = extrair_registros(arquivo, tipo_file)

                lote = []
                tam_lote = 1000
                linhas_lidas = 0
                linhas_gravadas = 0
    
    # Verifica schema e faz o load na entidade
                
                for linha in registros:
                    
                    linhas_lidas += 1

        # Define schema_validation com base na entidade

                    if entidade == "eventos":

                        nome, status, motivo = schema_event_validation(linha)

                    elif entidade == "produtos":

                        nome, status, motivo = schema_product_validation(linha)

                    elif entidade == "lojas":

                        nome, status, motivo = schema_store_validation(linha)

                    else:
                        print("schema de validação não encotrado pra essa entidade")

        # Verifica status do schema_validation
            
                    if not status == "VALIDO":                        

                        load_to_quarentine(
                            conexao_bd,
                            nome_arquivo,
                            linha,
                            entidade,
                            nome,
                            status,
                            motivo
                        )

                        nome_entidade = f"raw.{entidade}"
                        load_to_raw(conexao_bd, nome_arquivo, [linha], nome_entidade, nome, 'INVALIDO', 'quarentena')
                        conexao_bd.commit()

                    else:

                        lote.append(linha)
                    
    # Carrega lote na tabela raw.

                    if lote == tam_lote: # <- dentro do loop
                        
                        load = load_to_raw(conexao_bd, nome_arquivo, lote, entidade, nome, 'VALIDO', None)
                        conexao_bd.commit()
                        linhas_gravadas += len(lote)                            
                        lote.clear()
                
                if lote: # <- fora do loop

                    load_2 = load_to_raw(conexao_bd, nome_arquivo, lote, entidade, nome, 'VALIDO', None)
                    conexao_bd.commit()
                    linhas_gravadas += len(lote)
                    
                    lote.clear()

                if load_2:
                        
    # Move arquivos processados e finaliza a etapa de ingestão.

                    move = move_file(arquivo, path_processado)

                    if move:

                        fim = datetime.now()
                        diferenca = (fim - inicio_pipeline)
                        duracao   = diferenca.total_seconds()

        # Atualiza tabela audit.pipeline_step

                        reg_new_step(conexao_bd, id_exec, new_file, 'RAW', entidade, linhas_lidas, linhas_gravadas, inicio_pipeline, fim, duracao)
                        conexao_bd.commit()

                        return new_file, inicio_pipeline, entidade

    except Exception as e:
        print(f"Erro na etapa raw: {e}")