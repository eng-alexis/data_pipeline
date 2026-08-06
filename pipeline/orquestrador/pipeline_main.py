from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.raw.extract.extract_json import encontrar_arquivos, contar_registros
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.src.gold.gold_main import etapa_gold, etapa_gold_calendario

from pipeline.common.monitoring.pipeline_cycle import reg_pipeline_cycle, upd_pipeline_cycle
from pipeline.common.context.pipeline_context  import gerar_id_contexto, upd_watermark_exec
from pipeline.common.monitoring.pipeline_exec  import update_execution
from pipeline.common.monitoring.pipeline_exec  import reg_new_execution
from pipeline.common.monitoring.pipeline_step  import upd_step
from pipeline.common.database.conx_database import get_db_connection
from pipeline.common.database.conx_database import get_db_connection

from pipeline.common.exceptions.pipeline_exceptions import UnknownEntityException, DuplicateFileException
from pipeline.common.exceptions.pipeline_exceptions import  EmptyfileExcept, AllRecordsQuarantinedException, InsertRecordsFail

from pipeline.config.paths import PDV_NEW_FILES_DIR
from datetime import datetime

conx = get_db_connection()

path_padrão = PDV_NEW_FILES_DIR

tipos_esperados = ["jsonl", "json"]

print("""
+---------------- DATA PIPELINE ---------------+

▷ Ciclo iniciado
""")

conx = get_db_connection()

inicio_ciclo = datetime.now()
id_ciclo = reg_pipeline_cycle(conx, inicio_ciclo)

total_tamanho_files   = 0
total_arquivos_lidos  = 0
total_arquivos_processados = 0
total_qtde_registros = 0 
total_qtde_registros_invalidos = 0 

for tipo in tipos_esperados:

        arquivos_encontrados = encontrar_arquivos(path_padrão, tipo)

        for arquivo in arquivos_encontrados:

            total_arquivos_lidos += 1

            qtde_registros = contar_registros(arquivo, tipo)
            total_qtde_registros += qtde_registros

            tamanho_file = arquivo.stat().st_size
            total_tamanho_files += tamanho_file

            # Registra nova execução do pipeline na tabela de auditoria

            inicio_pipeline = datetime.now()
            id_exec = gerar_id_contexto(conx)
    
            reg_new_execution(conx, id_ciclo, id_exec, inicio_pipeline)
            conx.commit()

            try:

                etapa = "RAW"
                etapa_1 = etapa_raw(id_exec, arquivo)

                id_arquivo, nome_arquivo, entidade, reg_invalidos = etapa_1

                total_qtde_registros_invalidos += reg_invalidos

                etapa = "SILVER"
                etapa_2 = etapa_silver(id_exec, id_arquivo, entidade)
                etapa = "GOLD"
                etapa_3 = etapa_gold(id_exec, id_arquivo, entidade)
                etapa = "GOLD_CALENDARIO"
                etapa_4 = etapa_gold_calendario(id_exec, id_arquivo)

                fim_pipeline = datetime.now()

                update_execution(conx, id_exec, fim_pipeline, arquivo=nome_arquivo, status='SUCESSO',motivo=None, mensagem=None)
                upd_watermark_exec(conx, id_exec, fim_pipeline)

                total_arquivos_processados += 1


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
                
                print(f"""Etapa: {etapa} - Erro: {e}
                """)

fim_ciclo = datetime.now()
diferenca = (fim_ciclo - inicio_ciclo)
duracao   = int((diferenca.total_seconds()*1000))

print(f"""▶ Ciclo concluido

+------------------- Resumo -------------------+

• N° do ciclo                        = {id_ciclo}
• Duração (segundos) do ciclo        = {duracao/1000:.1f} segs
• Tamanho total dos arquivos (MB)    = {total_tamanho_files / (1024**2):.2f} MB
• Quantidade de arquivos encontrados = {total_arquivos_lidos}
• Quantidade de arquivos processados = {total_arquivos_processados}
• Quantidade de registros válidos    = {total_qtde_registros:,.0f}
• Quantidade de registros inválidos  = {total_qtde_registros_invalidos:,.0f}

+----------------------------------------------+

""")

upd_pipeline_cycle(conx, id_ciclo, fim_ciclo, duracao, total_arquivos_lidos, total_arquivos_processados, total_tamanho_files,
                    total_qtde_registros, total_qtde_registros_invalidos)

conx.commit()