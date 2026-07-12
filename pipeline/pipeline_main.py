from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.raw.extract.extract_json import encontrar_arquivos
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.src.gold.gold_main import etapa_gold, etapa_gold_calendario

from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.context.pipeline_context import gerar_id_contexto, upd_watermark_exec
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.common.monitoring.pipeline_exec import reg_new_execution
from pipeline.common.monitoring.pipeline_step import upd_step

from pipeline.config.paths import PDV_NEW_FILES_DIR
from datetime import datetime

from pipeline.common.exceptions.pipeline_exceptions import UnknownEntityException, DuplicateFileException, EmptyfileExcept, AllRecordsQuarantinedException, InsertRecordsFail

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

                id_arquivo, nome_arquivo, entidade = etapa_1

                etapa = "SILVER"
                etapa_2 = etapa_silver(id_exec, id_arquivo, entidade)
                etapa = "GOLD"
                etapa_3 = etapa_gold(id_exec, id_arquivo, entidade)
                etapa = "GOLD_CALENDARIO"
                etapa_4 = etapa_gold_calendario(id_exec, id_arquivo)

                fim_pipeline = datetime.now()

                update_execution(conx, id_exec, fim_pipeline, arquivo=nome_arquivo, status='SUCESSO',motivo=None, mensagem=None)
                upd_watermark_exec(conx, id_exec, fim_pipeline)


            except UnknownEntityException as e:
                inicio_step = e.inicio
                fim_pipeline = datetime.now()
                diferenca = (fim_pipeline - inicio_step)
                duracao = int((diferenca.total_seconds()*1000))

                update_execution(conx, id_exec, fim_pipeline, arquivo= e.arquivo, status=e.status, motivo=e.motivo, mensagem=e.mensagem)
                upd_watermark_exec(conx, id_exec, fim_pipeline)
                upd_step(conx, id_exec, fim_pipeline, e.status, 'RAW', e.entidade, duracao=duracao)
                 

            except DuplicateFileException as e:
                inicio_step = e.inicio
                fim_pipeline = datetime.now()
                diferenca = (fim_pipeline - inicio_step)
                duracao = int((diferenca.total_seconds()*1000))

                update_execution(conx, id_exec, fim_pipeline, arquivo= e.arquivo, status=e.status, motivo=e.motivo, mensagem=e.mensagem)
                upd_watermark_exec(conx, id_exec, fim_pipeline)
                upd_step(conx, id_exec, fim_pipeline, e.status, 'RAW', e.entidade, duracao=duracao)


            except EmptyfileExcept as e:      
                inicio_step = e.inicio
                fim_pipeline = datetime.now()
                diferenca = (fim_pipeline - inicio_step)
                duracao = int((diferenca.total_seconds()*1000))

                update_execution(conx, id_exec, fim_pipeline, arquivo= e.arquivo, status=e.status, motivo=e.motivo, mensagem=e.mensagem)
                upd_watermark_exec(conx, id_exec, fim_pipeline)
                upd_step(conx, id_exec, fim_pipeline, e.status, 'RAW', e.entidade, duracao=duracao)


            except AllRecordsQuarantinedException as e:   
                inicio_step = e.inicio
                fim_pipeline = datetime.now()
                diferenca = (fim_pipeline - inicio_step)
                duracao = int((diferenca.total_seconds()*1000))

                update_execution(conx, id_exec, fim_pipeline, arquivo= e.arquivo, status=e.status, motivo="REGISTROS_INVALIDOS", mensagem=e.mensagem)
                upd_watermark_exec(conx, id_exec, fim_pipeline)
                upd_step(conx, id_exec, fim_pipeline, e.status, 'RAW', e.entidade, duracao=duracao)

                     
            except InsertRecordsFail as e:
                inicio_step = e.inicio
                fim_pipeline = datetime.now()
                diferenca = (fim_pipeline - inicio_step)
                duracao = int((diferenca.total_seconds()*1000))

                update_execution(conx, id_exec, fim_pipeline, arquivo= e.arquivo, status=e.status, motivo=e.motivo, mensagem=e.mensagem)
                upd_watermark_exec(conx, id_exec, fim_pipeline)
                upd_step(conx, id_exec, fim_pipeline, e.status, 'RAW', e.entidade, duracao=duracao)

            except Exception as e:
                 
                inicio_step = inicio_pipeline
                fim_pipeline = datetime.now()
                diferenca = (fim_pipeline - inicio_step)
                duracao = int((diferenca.total_seconds()*1000))

                msg = f"{type(e).__name__}"

                update_execution(conx, id_exec, fim_pipeline, status="ERRO", motivo="UNEXPECTED_EXCEPTION",mensagem=msg)
                upd_watermark_exec(conx, id_exec, fim_pipeline)
                upd_step(conx, id_exec, fim_pipeline, "ERRO", 'RAW', duracao=duracao)
                
                print(f"Etapa: {etapa} - Erro: {e}")
             
print("Pipeline Concluido")