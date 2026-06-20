
from pipeline.src.silver.load.load_to_silver import get_ultimo_id, load_to_silver

from pipeline.common.context.pipeline_context import upd_watermark_exec, upd_watermark_layer
from pipeline.common.database.conx_database import get_db_connection

from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.common.monitoring.pipeline_step import reg_new_step

from pipeline.config.paths import SQL_SCRIPT_LOAD

from datetime import datetime

def etapa_silver(id_execution, id_arquivo, inicio_pipeline):

    try:
        conexao_db = get_db_connection()
        id_exec = id_execution
        inicio_step = datetime.now()

        # Carrega dados RAW -> SILVER

        sql_path = SQL_SCRIPT_LOAD

        ultimo_id = get_ultimo_id(conexao_db, 'raw.eventos_last_id')

        load = load_to_silver(conexao_db, ultimo_id, sql_path)

        linhas_lidas, linhas_gravadas = load

        # Atualiza id_contexto

        fim = datetime.now()
        upd_watermark_exec(conexao_db, id_exec, fim)

        # Atualiza o ultimo id da entidade raw (que já foi processado para silver)

        watermark = 'raw.eventos_last_id'
        fim = datetime.now()

        upd_watermark_layer(conexao_db, 'raw.eventos', watermark, fim)

        # Atualizar execução do pipeline

        fim = datetime.now()
        status = 'SUCESSO'
        msg = ''

        update_execution(conexao_db, id_exec, fim, status, msg)

        # Registra e Atualiza step silver

        camada = 'SILVER'
        entidade = 'silver.eventos'
        fim = datetime.now()

        diferenca = (fim - inicio_pipeline)
        duracao = diferenca.total_seconds()
        
        reg_new_step(conexao_db, id_exec, id_arquivo, camada, entidade, linhas_lidas, linhas_gravadas, inicio_step, fim, duracao)

        return True

    except Exception as e:
        print(f"Erro na etapa silver: {e}")