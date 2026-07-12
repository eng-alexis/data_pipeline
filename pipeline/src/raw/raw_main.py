from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_step import reg_new_step, upd_step
from pipeline.src.raw.extract.extract_json import extrair_registros,  is_file_empty, descobrir_entidade
from pipeline.src.raw.validate.validate_main import validate_schema
from pipeline.src.raw.file_control.hash import gerar_hash, find_hash
from pipeline.src.raw.file_control.manipulate_file import file_new_name, rename_file, move_file, delete_empty_dir
from pipeline.src.raw.file_control.register_file import reg_new_file
from pipeline.src.raw.load.load_raw import load_to_raw, load_to_quarentine

from pipeline.config.paths import PIPE_PROCESSED_FILES_DIR, PIPE_DUPLICATE_FILES_DIR, PIPE_INVALID_ENTITY_DIR, PIPE_EMPTY_FILES_DIR

from pipeline.common.exceptions.pipeline_exceptions import UnknownEntityException, DuplicateFileException, EmptyfileExcept, AllRecordsQuarantinedException, InsertRecordsFail

from datetime import datetime

# Diretorios

path_processado = PIPE_PROCESSED_FILES_DIR
path_duplicado  = PIPE_DUPLICATE_FILES_DIR
path_invalid_entity = PIPE_INVALID_ENTITY_DIR
path_empty_files = PIPE_EMPTY_FILES_DIR

# Conexão com banco pdv_sales

conexao_bd = get_db_connection()

def etapa_raw(id_execution, arquivo_original):

    # Inicia Pipeline

        inicio_step = datetime.now()
        id_exec = id_execution

        path_arquivo = arquivo_original
        nome_arquivo = file_new_name(path_arquivo, inicio_step)

        # Descobre e valida a entidade do arquivo

        TABELAS_RAW = {"eventos","produtos","lojas"}

        entidade = descobrir_entidade(path_arquivo)

        if entidade not in TABELAS_RAW:

            reject_file = rename_file(path_arquivo, datetime.now())
            move_file(reject_file, path_invalid_entity)
        
            raise UnknownEntityException(arquivo=nome_arquivo, entidade=entidade, inicio= inicio_step, 
                                            status="INTERROMPIDO", motivo='ENTIDADE_INVALIDA',
                                            mensagem="a entidade não é suportada")

        reg_new_step(conexao_bd, id_exec, 'RAW', inicio_step, entidade)

        # Descobre tipo de arquivo (json ou jsonl)

        tipo_file = "jsonl" if entidade == "eventos" else "json"

        # extrai informações 
                
        tamanho_bytes   = path_arquivo.stat().st_size
        hash_arquivo    = gerar_hash(path_arquivo)

        # Valida arquivo

        sh_file = find_hash(conexao_bd, hash_arquivo)

        # Aualiza tabela de auditoria, caso hash já exista no banco

        if sh_file:

            fim_step = datetime.now()
            
            path_arquivo = rename_file(path_arquivo,entidade, inicio_step)

            move_file(path_arquivo, path_duplicado)

            raise DuplicateFileException(arquivo=nome_arquivo, entidade=entidade, inicio= inicio_step, 
                                            status="INTERROMPIDO", motivo="ARQUIVO_DUPLICADO",
                                            mensagem=f"o arquivo {nome_arquivo} já foi processado anteriormente")

        else:

            lote = []
            tam_lote = 1000
            linhas_lidas = 0
            linhas_gravadas = 0
            
        if is_file_empty(path_arquivo):

            path_arquivo = rename_file(path_arquivo, entidade, inicio_step)
            move_file(path_arquivo, path_empty_files)

            raise EmptyfileExcept(arquivo=nome_arquivo, entidade=entidade, inicio= inicio_step, 
                                            status="INTERROMPIDO", motivo="ARQUIVO_VAZIO",
                                    mensagem=f"o arquivo {nome_arquivo} esta vazio.")
        
        # Extrai registros do arquivo

        registros = extrair_registros(path_arquivo, tipo_file)

        load_tentativa_1 = 0 
        load_tentativa_2 = 0

        try:

            for linha in registros:
                
                linhas_lidas += 1

                # Valida schema da linha

                version_schema, status, validation_error = validate_schema(linha, entidade)

                # Verifica status do schema_validation
        
                if status == "INVALIDO":
                        
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
                    
                elif status == "VALIDO":      

                    lote.append(linha)

                    # Carrega lote na tabela raw.

                if len(lote) == tam_lote:

                    load_tentativa_1 += 1
                    
                    load = load_to_raw(conexao_bd, nome_arquivo, lote, entidade, version_schema,'VALIDO', None)
                    linhas_gravadas += len(lote)                            
                    lote.clear()

            if lote:
                load_tentativa_2 += 1

                load_to_raw(conexao_bd, nome_arquivo, lote, entidade, version_schema,'VALIDO', None)
                linhas_gravadas += len(lote) 
                lote.clear()

            conexao_bd.commit()

        except Exception as e:

            conexao_bd.rollback()

            raise InsertRecordsFail(arquivo=nome_arquivo, entidade=entidade, inicio= inicio_step, 
                                                 status="INTERROMPIDO", motivo="FALHA_NO_LOAD_RAW",
                                                 mensagem=f"erro: {e}")

        if (load_tentativa_1 + load_tentativa_2) == 0:

            path_arquivo = rename_file(path_arquivo, entidade, inicio_step)

            move = move_file(path_arquivo, path_processado)

            raise AllRecordsQuarantinedException(arquivo=nome_arquivo, entidade=entidade, inicio= inicio_step, 
                                                 status="INTERROMPIDO", motivo="REGISTROS_INVALIDOS",
                                                 mensagem="todos os registros estão em quarentena")
        
        if not lote:
            
            # Registra arquivo na tabela de auditoria (audit.file_history)

            data_ingestao = datetime.now()
        
            id_arquivo = reg_new_file(conexao_bd, hash_arquivo, nome_arquivo,data_ingestao, tamanho_bytes, id_exec)    

            fim_step = datetime.now()
            diferenca = (fim_step - inicio_step)
            duracao   = int((diferenca.total_seconds()*1000))

            # Atualiza tabela audit.pipeline_step

            upd_step(conexao_bd, id_exec, fim_step, status='SUCESSO',camada='RAW', entidade=entidade, id_arquivo=id_arquivo,
                     linhas_lidas=linhas_lidas,linhas_gravadas=linhas_gravadas,duracao=duracao)

            conexao_bd.commit()
    
                            # Move arquivos processados e finaliza a etapa de ingestão.

            path_arquivo = rename_file(path_arquivo, entidade, inicio_step)

            move = move_file(path_arquivo, path_processado)

            if move:
                delete_empty_dir(path_arquivo)

            return  id_arquivo, nome_arquivo, entidade