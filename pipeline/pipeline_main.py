from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.src.gold.gold_main import etapa_gold, etapa_gold_calendario
from pipeline.common.context.pipeline_context import gerar_id_contexto
from pipeline.common.database.conx_database import get_db_connection
from pipeline.src.raw.extract.extract_json import encontrar_arquivos
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.src.raw.load.load_raw import descobrir_entidade
from pipeline.common.monitoring.pipeline_exec import reg_new_execution
from pipeline.config.paths import JSON_EVENTS_DIR
from datetime import datetime

conx = get_db_connection()

path_padrão = JSON_EVENTS_DIR

tipos_esperados = ["jsonl", "json"]

print("Pipeline Iniciado")

for tipo in tipos_esperados:

        arquivos_encontrados = encontrar_arquivos(path_padrão, tipo)

        for arquivo in arquivos_encontrados:

            inicio_pipeline = datetime.now()

            id_exec = gerar_id_contexto(conx)
            entidade = descobrir_entidade(arquivo)
            
            # Registra nova execução do pipeline na tabela de auditoria

            reg_new_execution(conx, id_exec, inicio_pipeline)
            conx.commit()

            try:
 
                etapa_1 = etapa_raw(id_exec, inicio_pipeline, arquivo, entidade)

                id_arquivo, nome_arquivo, hash_arquivo = etapa_1

                etapa_2 = etapa_silver(id_exec, id_arquivo, inicio_pipeline, entidade)
                etapa_3 = etapa_gold_calendario(id_exec, id_arquivo)
                etapa_4 = etapa_gold(id_exec, id_arquivo, entidade)

                fim_pipeline = datetime.now()

                update_execution(conx, id_exec, fim_pipeline, 'SUCESSO', arquivo=nome_arquivo, 
                                 hash=hash_arquivo)

            except Exception as e:

                fim_pipeline = datetime.now()
                msg = f"{type(e).__name__}"

                update_execution(conx, id_exec, fim_pipeline, 'ERRO', mensagem=msg )
                print(f"Erro: {e}")
             
print("Pipeline Concluido")