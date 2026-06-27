from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.src.gold.gold_main import etapa_gold
from pipeline.common.context.pipeline_context import gerar_id_contexto
from pipeline.common.database.conx_database import get_db_connection
from pipeline.src.raw.extract.extract_json import encontrar_arquivos
from pipeline.common.monitoring.pipeline_exec import update_execution
from pipeline.src.raw.load.load_raw import descobrir_entidade
from pipeline.src.raw.file_control.move_files import rename_file
from pipeline.config.paths import JSON_EVENTS_DIR
from datetime import datetime

conx = get_db_connection()

path_padrão = JSON_EVENTS_DIR

tipos_esperados = ["jsonl", "json"]

print("Pipeline Iniciado")

for tipo in tipos_esperados:

        arquivos_encontrados = encontrar_arquivos(path_padrão, tipo)

        for arquivo in arquivos_encontrados:

            inicio_secao = datetime.now()

            id_exec = gerar_id_contexto(conx)
            entidade = descobrir_entidade(arquivo)

            if entidade != "eventos":
                 
                 arquivo = rename_file(arquivo, inicio_secao)
                 print(arquivo)
            
            else:
                 arquivo
                 
            try:
 
                etapa_1 = etapa_raw(id_exec, inicio_secao, arquivo, entidade)

                etapa_2 = etapa_silver(id_exec, etapa_1, inicio_secao, entidade)
                
                etapa_3 = etapa_gold(id_exec, etapa_1, entidade)

                fim = datetime.now()

                update_execution(conx, id_exec, fim, 'SUCESSO', ' ')

            except Exception as e:

                fim = datetime.now()
                msg = f"{type(e).__name__}"
                update_execution(conx, id_exec, fim, 'ERRO', msg )

                print(f"Erro: {e}")
             
print("Pipeline Concluido")


