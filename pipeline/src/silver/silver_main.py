# Importa modulos

from pipeline.src.silver.load.load_to_silver import get_ultimo_id, load_to_silver, descobrir_script_sql
from pipeline.common.context.pipeline_context import upd_watermark_exec, upd_watermark_layer
from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.common.monitoring.pipeline_step import reg_new_step

from datetime import datetime

def etapa_silver(id_execution, id_arquivo, inicio_pipeline, entidade):

    try:
        conexao_db = get_db_connection()
        id_exec = id_execution
        inicio_step = datetime.now()

        # Carrega dados RAW -> SILVER

        sql_load_script = descobrir_script_sql(entidade)
        
        watermark_name = "raw.eventos_last_id"

        ultimo_id = get_ultimo_id(conexao_db, watermark_name)

        load = load_to_silver(conexao_db, ultimo_id, entidade ,sql_load_script)
        conexao_db.commit()

        # Atualiza id_contexto

        fim = datetime.now()
        upd_watermark_exec(conexao_db, id_exec, fim)

        # Atualiza ultimo id da entidade raw (que já foi processado pela etapa silver)

        fim = datetime.now()

        upd_watermark_layer(conexao_db, watermark_name, fim)

        # Atualizar id de execução do pipeline

        fim = datetime.now()
        status = 'SUCESSO'
        msg = ''

        update_execution(conexao_db, id_exec, fim, status, msg)

        # Registra e Atualiza step silver

        camada = 'SILVER'
        entidade_silver = f'silver.{entidade}'
        linhas_lidas, linhas_gravadas = load
        fim = datetime.now()
        diferenca = (fim - inicio_pipeline)
        duracao = diferenca.total_seconds()
        
        reg_new_step(conexao_db, id_exec, id_arquivo, camada, entidade_silver, linhas_lidas, linhas_gravadas, inicio_step, fim, duracao)
        
        return True

    except Exception as e:
        print(f"Erro na etapa silver: {e}")