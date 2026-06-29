from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.common.monitoring.pipeline_step import reg_new_step
from pipeline.common.context.pipeline_context import upd_watermark_exec

from pipeline.src.raw.extract.extract_json import extrair_registros, descobrir_entidade
from pipeline.src.raw.validate.schema_validate import schema_event_validation, schema_product_validation, schema_store_validation
from pipeline.src.raw.file_control.hash import gerar_hash, find_hash
from pipeline.src.raw.file_control.manipulate_file import rename_file, move_file, delete_empty_dir
from pipeline.src.raw.file_control.register_file import reg_new_file
from pipeline.src.raw.load.load_raw import load_to_raw, load_to_quarentine

from pipeline.config.paths import JSON_PROCESSED_DIR, JSON_DUPLICATE_DIR

from pathlib import Path
from datetime import datetime

# Diretorios

path_processado = JSON_PROCESSED_DIR
path_duplicado  = JSON_DUPLICATE_DIR

# Conexão com banco pdv_sales

conexao_bd = get_db_connection()

def etapa_raw(id_execution, inicio_pipeline, json_file):

    # Inicia Pipeline

    id_exec = id_execution
    arquivo = json_file

    # extrai informações 
    
    if entidade != "eventos":

        arquivo = rename_file(arquivo, inicio_pipeline)
    else:
        arquivo
                 
    hash_arquivo    = gerar_hash(arquivo)
    nome_arquivo    = Path(arquivo).name
    tamanho_bytes   = arquivo.stat().st_size

    # Valida arquivo

    sh_file  = find_hash(conexao_bd, hash_arquivo)
    
    # Aualiza tabela de auditoria, caso hash já exista no banco

    if sh_file:

        fim = datetime.now()

        upd_exec    = update_execution(conexao_bd, id_exec, fim, "DUPLICADO", mensagem="Hash já processado anteriormente")
        upd_id_exec = upd_watermark_exec(conexao_bd, id_exec, fim)
        conexao_bd.commit()

        # Move arquivo duplicado para pasta arq_duplicados

        move_file(arquivo, path_duplicado)

    # Registra novo arquivo na tabela de auditoria.

    else:

        # Descobre a entidade

        entidade = descobrir_entidade(arquivo)

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

            try:

                if entidade == "eventos":

                    nome, status, motivo = schema_event_validation(linha)

                elif entidade == "produtos":

                    nome, status, motivo = schema_product_validation(linha)

                elif entidade == "lojas":

                    nome, status, motivo = schema_store_validation(linha)

            except Exception as e:

                print(f"erro: {e}")

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

            if len(lote) == tam_lote:
                
                load = load_to_raw(conexao_bd, nome_arquivo, lote, entidade, nome, 'VALIDO', None)
                conexao_bd.commit()
                linhas_gravadas += len(lote)                            
                lote.clear()

        load_2 = False

        if lote:

            load_2 = load_to_raw(conexao_bd, nome_arquivo, lote, entidade, nome, 'VALIDO', None)
            conexao_bd.commit()
            linhas_gravadas += len(lote)
            
            lote.clear()

        if load_2:
                
            # Registra arquivo na tabela de auditoria (audit.file_history)

            data_ingestao = datetime.now()
        
            id_arquivo = reg_new_file(conexao_bd, hash_arquivo, nome_arquivo, data_ingestao, tamanho_bytes, id_exec)
            conexao_bd.commit()

        if id_arquivo:
    
            # Move arquivos processados e finaliza a etapa de ingestão.

                move = move_file(arquivo, path_processado)

                if move:
                    
                    delete_empty_dir(arquivo)
                    fim = datetime.now()
                    diferenca = (fim - inicio_pipeline)
                    duracao   = diferenca.total_seconds()

                    # Atualiza tabela audit.pipeline_step

                    reg_new_step(conexao_bd, id_exec, id_arquivo, 'RAW', entidade, linhas_lidas, linhas_gravadas, inicio_pipeline, fim, duracao)
                    conexao_bd.commit()

                    return id_arquivo, nome_arquivo, hash_arquivo, entidade