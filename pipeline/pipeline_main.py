from pipeline.src.raw.raw_main import etapa_raw
from pipeline.src.silver.silver_main import etapa_silver
from pipeline.common.context.pipeline_context import gerar_id_contexto
from pipeline.common.database.conx_database import get_db_connection
from pipeline.src.raw.extract.extract_json import encontrar_arquivos

conx = get_db_connection()

path_padrão     = "/home/alexis/data_pipeline/pipeline/testes/pos/"

jsonl_arquivo = encontrar_arquivos(path_padrão)



for arquivo in jsonl_arquivo:

    try:
        id_exec = gerar_id_contexto(conx)
        print(F"Pipeline id n° {id_exec} iniciado")

        sucesso = etapa_raw(id_exec, arquivo)

        if sucesso:

            print("1/2 - Etapa raw comcluida")

            arquivo, inicio = sucesso

            sucesso2 = etapa_silver(id_exec, arquivo, inicio)

            if sucesso2:

                print("2/2 - Etapa silver concluida")

                print("Pipeline Concluido")
                print("------------------")

    except Exception as e:
        print(f"Erro: {e}")

