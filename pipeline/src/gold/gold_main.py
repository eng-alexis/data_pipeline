from pipeline.src.gold.load.load_to_gold import load_to_gold

from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_step import reg_new_step, upd_step
from pipeline.common.context.pipeline_context import upd_watermark_layer
from pipeline.common.database.find_load_script import find_script_sql
from pipeline.common.context.pipeline_context import get_ultimo_id, get_ultimo_id_tabela

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
    ultimo_id_before = get_ultimo_id_tabela(conexao, 'id_fato', 'gold.fato_vendas')

    sql_load_script = find_script_sql(entidade, "gold")
    watermark_name = "silver.eventos_last_id"
    last_id_silver  = get_ultimo_id(conexao, watermark_name)
    linhas_lidas = load_to_gold(conexao, sql_load_script, last_id_silver)
 
    fim_step = datetime.now()
    diferenca = (fim_step - inicio_step)
    duracao = diferenca.total_seconds()

    ultimo_id_after = get_ultimo_id_tabela(conexao, 'id_fato', 'gold.fato_vendas')
    linhas_gravadas = (ultimo_id_after - ultimo_id_before)

    upd_step(conection_db=conexao, id_exec=id_execucao, fim=fim_step, status='SUCESSO', camada='GOLD',entidade=entidade_gold,
              id_arquivo=id_arquivo, linhas_lidas=linhas_lidas, linhas_gravadas=linhas_gravadas, duracao=duracao)
    
    upd_watermark_layer(conexao, "id_silver", "silver.eventos", watermark_name, fim_step)

    return True

# Carrega registros de data na dim_calendario do schema gold

def etapa_gold_calendario(id_execucao, id_arquivo):

    inicio_step = datetime.now()
    conexao = get_db_connection()

    reg_new_step(conexao, id_execucao, 'GOLD', inicio_step, 'dim_calendario')
    ultimo_id_before = get_ultimo_id_tabela(conexao, 'id_calendario', 'gold.dim_calendario')

    sql_load_script = SQL_LOAD_TO_DIM_CALENDARIO
    watermark_name = "gold.fato_vendas_last_id"
    ultimo_id = get_ultimo_id(conexao, watermark_name)
    linhas_lidas = load_to_gold(conexao, sql_load_script, ultimo_id)

    fim_step = datetime.now()
    diferenca = (fim_step - inicio_step)
    duracao = diferenca.total_seconds()

    ultimo_id_after = get_ultimo_id_tabela(conexao, 'id_calendario', 'gold.dim_calendario')
    linhas_gravadas = (ultimo_id_after - ultimo_id_before)

    upd_step(conection_db=conexao, id_exec=id_execucao, fim=fim_step, status='SUCESSO', camada='GOLD',entidade='dim_calendario',
              id_arquivo=id_arquivo, linhas_lidas=linhas_lidas, linhas_gravadas=linhas_gravadas, duracao=duracao)
    
    upd_watermark_layer(conexao, "id_fato", "gold.fato_vendas", watermark_name, fim_step)

    return True