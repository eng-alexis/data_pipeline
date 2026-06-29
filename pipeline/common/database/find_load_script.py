from pipeline.config.paths import SQL_LOAD_TO_EVENTOS, SQL_LOAD_TO_LOJAS, SQL_LOAD_TO_PRODUTOS
from pipeline.config.paths import SQL_LOAD_TO_FATO_VENDAS, SQL_LOAD_TO_DIM_LOJAS, SQL_LOAD_TO_DIM_PRODUTOS

# Retorna o script sql correto com base na entidade

def find_script_sql(entidade, camada):

    if entidade == "eventos":
        if camada == "silver":
            return SQL_LOAD_TO_EVENTOS
        else:
            return SQL_LOAD_TO_FATO_VENDAS
    
    elif entidade == "produtos":
        if camada == "silver":
            return SQL_LOAD_TO_PRODUTOS
        else:
            return SQL_LOAD_TO_DIM_PRODUTOS

    elif entidade == "lojas":
        if camada == "silver":
            return SQL_LOAD_TO_LOJAS
        else:
            return SQL_LOAD_TO_DIM_LOJAS

    else:
        return print(f"Script sql não encontrado para essa entidade {entidade}")