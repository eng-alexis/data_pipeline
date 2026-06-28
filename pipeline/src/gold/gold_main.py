from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_step import reg_new_step
from pipeline.src.gold.load.load_to_gold import get_ultimo_id, find_script_sql, load_to_gold, upd_watermark
from pipeline.config.paths import SQL_LOAD_TO_DIM_CALENDARIO
from datetime import datetime

def etapa_gold(id_execucao, id_arquivo, entidade):
    
    inicio = datetime.now()

    conexao = get_db_connection()

    script = find_script_sql(entidade)

    ultimo_id = get_ultimo_id(conexao)

    linhas_lidas, linhas_gravadas = load_to_gold(conexao, script, ultimo_id)

    fim = datetime.now()
    diferenca = (fim - inicio)
    duracao = diferenca.total_seconds()

    upd_watermark(conexao)

    reg_new_step(conexao, id_execucao, id_arquivo, 'GOLD', entidade, linhas_lidas, linhas_gravadas, inicio, fim, duracao)

    return True

def etapa_gold_calendario(id_execucao, id_arquivo):
    
    inicio = datetime.now()

    conexao = get_db_connection()

    script = SQL_LOAD_TO_DIM_CALENDARIO

    ultimo_id = get_ultimo_id(conexao)

    linhas_lidas, linhas_gravadas = load_to_gold(conexao, script, ultimo_id)

    fim = datetime.now()
    diferenca = (fim - inicio)
    duracao = diferenca.total_seconds()

    reg_new_step(conexao, id_execucao, id_arquivo, 'GOLD', 'Calendario', linhas_lidas, linhas_gravadas, inicio, fim, duracao)

    return True
