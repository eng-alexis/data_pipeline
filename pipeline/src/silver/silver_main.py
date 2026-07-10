from pipeline.src.silver.load.load_to_silver import load_to_silver
from pipeline.common.database.find_load_script import find_script_sql
from pipeline.common.context.pipeline_context import get_ultimo_id, upd_watermark_layer
from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_step import reg_new_step, upd_step

from datetime import datetime

# Carrega registros nas tabelas do schema silver

def etapa_silver(id_execution, id_arquivo, entidade):

    inicio_step = datetime.now()
    conexao_db = get_db_connection()
    entidade_silver = f'silver.{entidade}'

    reg_new_step(conexao_db, id_execution, 'SILVER', inicio_step, entidade_silver)

    sql_load_script = find_script_sql(entidade, "silver")
    watermark_name = "raw.eventos_last_id"
    last_id_raw = get_ultimo_id(conexao_db, watermark_name)
    linhas_lidas, linhas_gravadas = load_to_silver(conexao_db, last_id_raw, entidade,
                                                   sql_load_script)
    fim_step = datetime.now()
    diferenca = (fim_step - inicio_step)
    duracao = diferenca.total_seconds()

    upd_step(conexao_db, id_execution, 'SILVER', fim_step, 'SUCESSO', duracao, id_arquivo, entidade_silver, linhas_lidas, linhas_gravadas)

    upd_watermark_layer(conexao_db, "id_raw", "raw.eventos", watermark_name, fim_step)

    
    return True