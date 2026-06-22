from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.common.context.pipeline_context import gerar_id_contexto
from pipeline.common.database.conx_database import get_db_connection
from pipeline.src.raw.extract.extract_json import encontrar_arquivos
from pipeline.config.paths import JSON_EVENTS_DIR

conx = get_db_connection()

path_padrão = JSON_EVENTS_DIR

tipos_esperados = ["jsonl", "json"]

print("Pipeline Iniciado")

for tipo in tipos_esperados:

    arquivos_encontrados = encontrar_arquivos(path_padrão, tipo)

    arquivos_raw = 0
    arquivos_silver = 0

    for arquivo in arquivos_encontrados:

        try:
            id_exec = gerar_id_contexto(conx)

            sucesso = etapa_raw(id_exec, arquivo)

            arquivos_raw += 1

            if sucesso:

                arquivo, inicio, entidade = sucesso

                sucesso2 = etapa_silver(id_exec, arquivo, inicio, entidade)

                if sucesso2:

                    arquivos_silver += 1

        except Exception as e:
            print(f"Erro: {e}")

print("Pipeline Concluido")