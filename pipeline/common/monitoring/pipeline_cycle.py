# Registra inicio do ciclo

def reg_pipeline_cycle(conexao_bd, inicio):

    cursor = conexao_bd.cursor()
    
    query = """INSERT INTO audit.pipeline_cycle (inicio_cycle, status)
                VALUES(%s, 'PROCESSANDO');"""
    
    valores = inicio
    
    cursor.execute(query, (valores,))

    query_2 = """SELECT MAX(id_cycle) FROM audit.pipeline_cycle;"""
    cursor.execute(query_2)

    id_cycle = cursor.fetchone()[0]

    return id_cycle

# Atualiza informações no final do ciclo


def upd_pipeline_cycle(conexao_bd, id_cycle, fim_cycle, duracao, qtde_arquivos, qtde_arquivos_processados, tamanho_bytes, qtde_registros, qtde_registros_invalidos):

    cursor = conexao_bd.cursor()

    query = """UPDATE audit.pipeline_cycle
                SET fim_cycle = %s, duracao_ms = %s, qtde_arquivos_lidos = %s, qtde_arquivos_processados = %s,
                tamanho_bytes = %s, qtde_registros = %s, qtde_registros_invalidos = %s, status = 'SUCESSO'
                WHERE id_cycle = %s;"""
    
    valores = (fim_cycle, duracao, qtde_arquivos, qtde_arquivos_processados, tamanho_bytes, qtde_registros, qtde_registros_invalidos, id_cycle)

    cursor.execute(query, valores)