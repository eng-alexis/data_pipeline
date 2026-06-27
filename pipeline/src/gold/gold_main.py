from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_step import reg_new_step
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.src.gold.load.load_to_gold import get_ultimo_id, find_script_sql, load_to_gold, upd_watermark

from datetime import datetime

def etapa_gold(id_exec, id_arquivo, entidade):
    
    try:

        inicio = datetime.now()

        conexao = get_db_connection()

        script = find_script_sql(entidade)

        ultimo_id = get_ultimo_id(conexao)

        linhas_lidas, linhas_gravadas = load_to_gold(conexao, script, ultimo_id)

        fim = datetime.now()
        diferenca = (fim - inicio)
        duracao = diferenca.total_seconds()

        upd_watermark(conexao)

        fim = datetime.now()
        status = 'SUCESSO'
        msg = ''

        update_execution(conexao, id_exec, fim, status, msg)

        reg_new_step(conexao, id_exec, id_arquivo, 'GOLD', entidade, linhas_lidas, linhas_gravadas, inicio, fim, duracao)

        return True

    except Exception as e:
        print(f"Erro na etapa gold: {e}")