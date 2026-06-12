from pipeline.common.database.conx_database import get_db_connection

from pipeline.src.raw.extract.extract_json import encontrar_arquivos, extrair_registros
from pipeline.src.raw.file_control.search_file_hist import gerar_hash, find_hash
from pipeline.src.raw.file_control.move_files import reg_new_execution, reg_novo_arquivo, update_execution, move_file
from pipeline.src.raw.moni
from pipeline.src.raw.load.load_raw import load_to_raw

from pathlib import Path
from datetime import datetime

# Diretorios e utilitarios

path_padrão     = "/home/alexis/data_pipeline/pipeline/testes/"
path_processado = "/home/alexis/data_pipeline/pipeline/arquivos_processados/"

conexao_bd = get_db_connection()
cursor     = conexao_bd.cursor()
contador   = 1

# Inicia Pipeline

jsonl_arquivo = encontrar_arquivos(path_padrão)

for arquivo in jsonl_arquivo:

# Registra nova execução do pipeline na tabela de auditoria

    new_exec = reg_new_execution(conexao_bd, inicio, nome_arquivo, hash_arquivo)

# extrai informações e valida arquivo

    inicio        = datetime.now()
    hash_arquivo  = gerar_hash(arquivo)
    nome_arquivo  = Path(arquivo).name
    tamanho_bytes = arquivo.stat().st_size

    sh_file  = find_hash(conexao_bd, hash_arquivo)
    
# Aualiza tabela de auditoria, caso hash já exista no banco

    if sh_file:

        parada = datetime.now()
        upd_exec = update_execution(parada, conexao_bd, contador, "DUPLICADO", "Hash já processado anteriormente")

# Registra novo arquivo na tabela de auditoria.

    else:

        new_file = reg_novo_arquivo(conexao_bd, hash_arquivo, nome_arquivo, tamanho_bytes, contador)
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
                    update_execution(fim, conexao_bd, contador, 'SUCESSO','')
    
    contador += 1