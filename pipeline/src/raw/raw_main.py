    # Importa funções

from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_exec import reg_new_execution, update_execution
from pipeline.common.monitoring.pipeline_step import reg_new_step
from pipeline.common.context.pipeline_context import upd_watermark_exec

from pipeline.src.raw.extract.extract_json import extrair_registros
from pipeline.src.raw.file_control.search_file_hist import gerar_hash, find_hash
from pipeline.src.raw.file_control.move_files import reg_novo_arquivo, move_file
from pipeline.src.raw.load.load_raw import load_to_raw

from pathlib import Path
from datetime import datetime

path_processado = "/home/alexis/data_pipeline/pipeline/testes/arq_processados/"

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

        entidade        = "raw.eventos"

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
            print("Alerta !")
            print(f"Arquivo duplicado")
            print("Pipeline Interrompido")
            print("------------------")

    # Registra novo arquivo na tabela de auditoria.

        else:

            data_ingestao = datetime.now()
            
            new_file = reg_novo_arquivo(conexao_bd, hash_arquivo, nome_arquivo, data_ingestao, tamanho_bytes, id_exec)
            conexao_bd.commit()

            if new_file:
                
    # Extrai registros e cria Lote.

                registros = extrair_registros(arquivo)

                lote = []
                tam_lote = 1000
                qtd_lote = 0
                linhas_lidas = 0
                linhas_gravadas = 0
                
                for linha in registros:
                    linhas_lidas += 1

                    lote.append(linha)
                    
    # Carrega lote na tabela raw.

                    if len(lote) == tam_lote:
                        
                        load = load_to_raw(conexao_bd, nome_arquivo, lote)
                        conexao_bd.commit()
                        linhas_gravadas += len(lote)
                        lote.clear()
                        qtd_lote += 1
                
                if lote:

                    load = load_to_raw(conexao_bd, nome_arquivo, lote)
                    conexao_bd.commit()
                    linhas_gravadas += len(lote)
                    qtd_lote += 1
                    lote.clear()

                if load:

    # Move arquivos processados e finaliza a etapa de ingestão.

                    move = move_file(arquivo, path_processado)

                    if move:

                        fim = datetime.now()
                        diferenca = (fim - inicio_pipeline)
                        duracao   = diferenca.total_seconds()

    # Atualiza tabela audit.pipeline_step

                        reg_new_step(conexao_bd, id_exec, new_file, 'RAW', entidade, linhas_lidas, linhas_gravadas, inicio_pipeline, fim, duracao)
                        conexao_bd.commit()

                        return new_file, inicio_pipeline

    except Exception as e:
        print(f"Erro na etapa raw: {e}")