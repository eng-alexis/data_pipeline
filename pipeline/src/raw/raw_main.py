from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_exec import reg_new_execution, update_execution
from pipeline.common.context.pipeline_context import gerar_id_contexto, upd_watermark_exec, upd_watermark_layer

from pipeline.src.raw.extract.extract_json import encontrar_arquivos, extrair_registros
from pipeline.src.raw.file_control.search_file_hist import gerar_hash, find_hash
from pipeline.src.raw.file_control.move_files import reg_novo_arquivo, move_file
from pipeline.src.raw.load.load_raw import load_to_raw

from pathlib import Path
from datetime import datetime

# Diretorios e utilitarios

path_padrão     = "/home/alexis/data_pipeline/pipeline/testes/"
path_processado = "/home/alexis/data_pipeline/pipeline/arquivos_processados/"

conexao_bd = get_db_connection()
cursor     = conexao_bd.cursor()

jsonl_arquivo = encontrar_arquivos(path_padrão)

for arquivo in jsonl_arquivo:

# Inicia Pipeline

    id_exec = gerar_id_contexto(conexao_bd)
    print(f"id atual {id_exec}")

# extrai informações 

    inicio        = datetime.now()
    hash_arquivo  = gerar_hash(arquivo)
    nome_arquivo  = Path(arquivo).name
    tamanho_bytes = arquivo.stat().st_size

# Registra nova execução do pipeline na tabela de auditoria

    new_exec = reg_new_execution(conexao_bd, id_exec, inicio, nome_arquivo, hash_arquivo)
    conexao_bd.commit()

# Valida arquivo

    sh_file  = find_hash(conexao_bd, hash_arquivo)
    
# Aualiza tabela de auditoria, caso hash já exista no banco

    if sh_file:

        fim = datetime.now()
        upd_exec = update_execution(conexao_bd, id_exec, fim, "DUPLICADO", "Hash já processado anteriormente")
        upd_id_exec = upd_watermark_exec(conexao_bd, id_exec, fim)
        conexao_bd.commit()
        
        print(f"Arquivo {nome_arquivo} já foi processado anteriormente")

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
            qtd_registros = 0
            
            for linha in registros:

                lote.append(linha)
                
# Carrega lote na tabela raw.

                if len(lote) == tam_lote:
                    
                    load = load_to_raw(conexao_bd, nome_arquivo, lote)
                    conexao_bd.commit()
                    qtd_registros += len(lote)
                    lote.clear()
                    qtd_lote += 1
            
            if lote:

                load = load_to_raw(conexao_bd, nome_arquivo, lote)
                conexao_bd.commit()
                qtd_registros += len(lote)
                qtd_lote += 1
                lote.clear()

            if load:

# Move arquivos processados e finaliza a etapa de ingestão.

                move = move_file(arquivo, path_processado)

                if move:
                    fim = datetime.now()
                    update_execution(conexao_bd, id_exec, fim, 'SUCESSO','')
                    upd_watermark_exec(conexao_bd, id_exec, fim)
                    conexao_bd.commit()

                    print("Pipeline Concluido")
                    print(f"Registros carregados: {qtd_registros}")