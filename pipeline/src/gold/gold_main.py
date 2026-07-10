from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_step import reg_new_step, upd_step
from pipeline.src.gold.load.load_to_gold import load_to_gold
from pipeline.common.context.pipeline_context import upd_watermark_layer
from pipeline.common.database.find_load_script import find_script_sql
from pipeline.common.context.pipeline_context import get_ultimo_id
from pipeline.config.paths import SQL_LOAD_TO_DIM_CALENDARIO

from datetime import datetime

# Carrega registros nas tabelas do schema gold

def etapa_gold(id_execucao, id_arquivo, entidade):
    
    inicio_step = datetime.now()
    conexao = get_db_connection()
    if entidade == "eventos":
        entidade_gold = "fato_vendas"
    else:
        entidade_gold = f"dim_{entidade}"

    reg_new_step(conexao, id_execucao, 'GOLD', inicio_step, entidade_gold)

    sql_load_script = find_script_sql(entidade, "gold")
    watermark_name = "silver.eventos_last_id"
    last_id_silver  = get_ultimo_id(conexao, watermark_name)
    linhas_lidas, linhas_gravadas = load_to_gold(conexao, sql_load_script, last_id_silver)

    fim_step = datetime.now()
    diferenca = (fim_step - inicio_step)
    duracao = diferenca.total_seconds()

    upd_step(conexao, id_execucao, 'GOLD', fim_step, 'SUCESSO', duracao, id_arquivo, entidade_gold, linhas_lidas, linhas_gravadas)

    upd_watermark_layer(conexao, "id_silver", "silver.eventos", watermark_name, fim_step)

    
    return True

# Carrega registros de data na dim_calendario do schema gold

def etapa_gold_calendario(id_execucao, id_arquivo):
    
    inicio_step = datetime.now()
    conexao = get_db_connection()

    reg_new_step(conexao, id_execucao, 'GOLD', inicio_step, 'dim_calendario')

    sql_load_script = SQL_LOAD_TO_DIM_CALENDARIO
    watermark_name = "silver.eventos_last_id"
    last_id_silver = get_ultimo_id(conexao, watermark_name)
    linhas_lidas, linhas_gravadas = load_to_gold(conexao, sql_load_script, last_id_silver)

    fim_step = datetime.now()
    diferenca = (fim_step - inicio_step)
    duracao = diferenca.total_seconds()

    upd_step(conexao, id_execucao, 'GOLD', fim_step, 'SUCESSO', duracao, id_arquivo, 'dim_calendario', linhas_lidas, linhas_gravadas)

    return True