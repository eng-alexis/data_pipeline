from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_step import reg_new_step
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.src.gold.load.load_to_gold import get_ultimo_id, find_script_sql, load_to_gold, upd_watermark

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