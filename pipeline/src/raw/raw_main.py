from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.common.monitoring.pipeline_step import reg_new_step
from pipeline.common.context.pipeline_context import upd_watermark_exec
from pipeline.src.raw.extract.extract_json import extrair_registros, descobrir_entidade
from pipeline.src.raw.validate.schema_validate import schema_event_validation, schema_product_validation, schema_store_validation
from pipeline.src.raw.validate.validate_main import validate_schema
from pipeline.src.raw.file_control.hash import gerar_hash, find_hash
from pipeline.src.raw.file_control.manipulate_file import rename_file, move_file, delete_empty_dir
from pipeline.src.raw.file_control.register_file import reg_new_file
from pipeline.src.raw.load.load_raw import load_to_raw, load_to_quarentine

from pipeline.config.paths import PIPE_PROCESSED_FILES_DIR, PIPE_DUPLICATE_FILES_DIR

from pathlib import Path
from datetime import datetime

# Diretorios

path_processado = PIPE_PROCESSED_FILES_DIR
path_duplicado  = PIPE_DUPLICATE_FILES_DIR

# Conexão com banco pdv_sales

conexao_bd = get_db_connection()

def etapa_raw(id_execution, json_file):

    # Inicia Pipeline

    inicio_step = datetime.now()

    id_exec = id_execution
    arquivo = json_file

    # Descobre e valida a entidade do arquivo

    entidade = descobrir_entidade(arquivo)

    TABELAS_RAW = {"eventos","produtos","lojas"}

    if entidade not in TABELAS_RAW:
        raise ValueError(f"Entidade inválida: {entidade}")

    # Descobre tipo de arquivo (json ou jsonl)
    
    if entidade == "eventos":
        tipo_file = "jsonl"

    else:
        tipo_file = "json"

    # extrai informações 
               
    tamanho_bytes   = arquivo.stat().st_size
    hash_arquivo    = gerar_hash(arquivo)

    # Valida arquivo

    sh_file = find_hash(conexao_bd, hash_arquivo)

    
    # Aualiza tabela de auditoria, caso hash já exista no banco

    if sh_file:

        fim_step = datetime.now()

        upd_exec = update_execution(conexao_bd, id_exec, fim_step, "DUPLICADO", 
                                       mensagem="Hash já processado anteriormente")
        
        upd_id_exec = upd_watermark_exec(conexao_bd, id_exec, fim_step)
        conexao_bd.commit()

        if entidade != "eventos":

            arquivo = rename_file(arquivo, inicio_step)
        else:
            arquivo

        nome_arquivo = Path(arquivo).name

        # Move arquivo duplicado para pasta arq_duplicados

        move_file(arquivo, path_duplicado)

        return 'DUPLICADO', 'None', nome_arquivo, hash_arquivo, entidade


    # Registra novo arquivo na tabela de auditoria.

    else:

        registros = extrair_registros(arquivo, tipo_file)

        lote = []
        tam_lote = 1000
        linhas_lidas = 0
        linhas_gravadas = 0
        

        # Verifica schema e faz o load na entidade
        
        try:

            nome_arquivo = Path(arquivo).name

            for linha in registros:
                
                linhas_lidas += 1

                # Valida schema da linha

                try:

                     version_schema, status, validation_error = validate_schema(linha, entidade)

                except Exception as e:

                    print(f"erro: {e}")

                # Verifica status do schema_validation
        
                if not status == "VALIDO":
                        
                    load_to_quarentine(
                        conexao_bd,
                        nome_arquivo,
                        linha,
                        entidade,
                        version_schema,
                        status,
                        validation_error)
                    

                    nome_entidade = f"raw.{entidade}"
                    load_to_raw(conexao_bd, nome_arquivo, [linha], nome_entidade, version_schema,
                                'INVALIDO', 'Em quarentena')
                    
                else:       

                    lote.append(linha)

                    # Carrega lote na tabela raw.
            
                if len(lote) == tam_lote:
                    
                    load = load_to_raw(conexao_bd, nome_arquivo, lote, entidade, version_schema,
                                        'VALIDO', None)
                    #conexao_bd.commit()
                    linhas_gravadas += len(lote)                            
                    lote.clear()

            if lote:

                load_to_raw(conexao_bd, nome_arquivo, lote, entidade, version_schema,
                            'VALIDO', None)

                #conexao_bd.commit()
        
                linhas_gravadas += len(lote) 

                lote.clear()
        
            if not lote:
                
                # Registra arquivo na tabela de auditoria (audit.file_history)

                data_ingestao = datetime.now()
            
                id_arquivo = reg_new_file(conexao_bd, hash_arquivo, nome_arquivo,
                                        data_ingestao, tamanho_bytes, id_exec)    

                fim_step = datetime.now()
                diferenca = (fim_step - inicio_step)
                duracao   = diferenca.total_seconds()

                conexao_bd.commit()

                # Atualiza tabela audit.pipeline_step

                reg_new_step(conexao_bd, id_exec, id_arquivo, 'RAW', entidade,
                            linhas_lidas, linhas_gravadas, inicio_step, fim_step,
                                duracao)
                
                conexao_bd.commit()

                # Move arquivos processados e finaliza a etapa de ingestão.

                move = move_file(arquivo, path_processado)

                if move:
                    
                    delete_empty_dir(arquivo)

                    return 'SUCESSO', id_arquivo, nome_arquivo, hash_arquivo, entidade
        
        except Exception:
            conexao_bd.rollback()
            raise