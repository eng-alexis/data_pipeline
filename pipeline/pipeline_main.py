from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.src.gold.gold_main import etapa_gold, etapa_gold_calendario

from pipeline.src.raw.extract.extract_json import encontrar_arquivos
from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.context.pipeline_context import gerar_id_contexto, upd_watermark_exec
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.common.monitoring.pipeline_exec import reg_new_execution

from pipeline.config.paths import PDV_NEW_FILES_DIR
from datetime import datetime

conx = get_db_connection()

path_padrão = PDV_NEW_FILES_DIR

tipos_esperados = ["jsonl", "json"]

print("Pipeline Iniciado")

for tipo in tipos_esperados:

        arquivos_encontrados = encontrar_arquivos(path_padrão, tipo)

        for arquivo in arquivos_encontrados:

            # Registra nova execução do pipeline na tabela de auditoria

            inicio_pipeline = datetime.now()
            id_exec = gerar_id_contexto(conx)
    
            reg_new_execution(conx, id_exec, inicio_pipeline)
            conx.commit()

            try:

                etapa = "RAW"
                etapa_1 = etapa_raw(id_exec, arquivo)

                status, id_arquivo, nome_arquivo, hash_arquivo, entidade = etapa_1

                if status == 'SUCESSO':

                    etapa = "SILVER"
                    etapa_2 = etapa_silver(id_exec, id_arquivo, entidade)
                    etapa = "GOLD_CALENDARIO"
                    etapa_3 = etapa_gold_calendario(id_exec, id_arquivo)
                    etapa = "GOLD"
                    etapa_4 = etapa_gold(id_exec, id_arquivo, entidade)

                    fim_pipeline = datetime.now()

                    update_execution(conx, id_exec, fim_pipeline, status, arquivo=nome_arquivo, 
                                    hash=hash_arquivo)
                            
                    upd_watermark_exec(conx, id_exec, fim_pipeline)
                
                else:

                    fim_pipeline = datetime.now()
                    msg = "Arquivo duplicado"
                    update_execution(conx, id_exec, fim_pipeline, 'SUCESSO', arquivo=nome_arquivo, mensagem= msg, 
                                    hash=hash_arquivo)
                            
                    upd_watermark_exec(conx, id_exec, fim_pipeline)
                     

            except Exception as e:

                fim_pipeline = datetime.now()
                msg = f"{type(e).__name__}"

                update_execution(conx, id_exec, fim_pipeline, 'ERRO', arquivo=nome_arquivo, mensagem=msg )
                upd_watermark_exec(conx, id_exec, fim_pipeline)
                
                print(f"Etapa: {etapa} - Erro: {e} - File: {nome_arquivo}")
             
print("Pipeline Concluido")