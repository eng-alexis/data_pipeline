from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.common.context.pipeline_context import gerar_id_contexto
from pipeline.common.database.conx_database import get_db_connection
from pipeline.src.raw.extract.extract_json import encontrar_arquivos
from pipeline.config.paths import JSON_EVENTS_DIR

conx = get_db_connection()

path_padrão = JSON_EVENTS_DIR

tipos_esperados = ["jsonl", "json"]

for tipo in tipos_esperados:

    arquivos_encontrados = encontrar_arquivos(path_padrão, tipo)

    for arquivo in arquivos_encontrados:

        try:
            id_exec = gerar_id_contexto(conx)
            print(F"Pipeline id n° {id_exec} iniciado")

            sucesso = etapa_raw(id_exec, arquivo)

            if sucesso:

                print("1/2 - Etapa raw comcluida")

                arquivo, inicio, entidade = sucesso

                sucesso2 = etapa_silver(id_exec, arquivo, inicio, entidade)

                if sucesso2:

                    print("2/2 - Etapa silver concluida")

                    print("Pipeline Concluido")
                    print("------------------")

        except Exception as e:
            print(f"Erro: {e}")