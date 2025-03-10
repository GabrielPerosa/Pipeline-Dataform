import re
import os
from files import load_files, get_content
from google.cloud import bigquery
from sql_treatment import sql_treatment

dates = ['2024-01-01', '2025-02-01', '2025-03-01','2025-05-01']
project_id = 'integracaohomologado'
sql_folder = './sql_files_for_tests'

def create_sql_for_validate(content, file_name):
    """
    OBJETIVO: Criar um arquivo SQL para validar se a tabela existe.

    PARâMETROS: O conteúdo que passará por validação e o nome do arquivo.
        Converte código SQLX para SQL do BigQuery, removendo declarações de variáveis.

    Returns:
        str: O nome do arquivo gravado
    """
    # Padrão para encontrar código SQL
    pattern = r"pre_operations(.*?)post_operations"

    # busca a incidencia no conteudo
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # obter codigo
        sql_code = match.group() 
        lines = sql_code.splitlines()
        # remove linhas desnecessárias
        sql_cleaned = '\n'.join(lines[1:-1])
        # Cria a pasta para armazenar SQLs
        if not os.path.exists(sql_folder):
            os.makedirs(sql_folder)
        file_name = file_name.replace("sqlx", "sql")
        path = './sql_files_for_tests/{}'.format(file_name)
    else:
        print("Não houve correspondencia")
        return None
 
    try:
        # Grava arquivo para realizar teste
        with open(path, "w", encoding="utf-8") as file:
            file.write(sql_cleaned)
            print("Gravado com Sucesso:\033[33m {} \033[0m".format(file_name))
            file.close()
        return file_name
    except Exception as e:
            return e
            


def sql_cost_validation(content, file_name):
    """
        Realiza tratamento adicional no código SQL e o envia para a API BigQuery
        para avaliar custo estimado de processamento da consulta
    
    Args:
        content (str): Conteudo a ser gravado.
        file_name (str): Nome do arquivo a ser gravado.
    """

    # Criando arquivo SQL base
    file_created_name = create_sql_for_validate(content, file_name)
    if(file_created_name != None):
        sql_folder_path = '{}/'.format(sql_folder)
        content = get_content(sql_folder_path, file_created_name)
    else:
        print("erro")
        return
    # Realizando tratamentos nos arquivos
    sql_code = sql_treatment(content, dates)
    print(sql_code)
    # Abrindo cliente BigQuery
    client = bigquery.Client(project=project_id)
    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)
    query_job = client.query((sql_code), job_config)
    mb_processed = query_job.total_bytes_processed/pow(1024,2)
    mb_processed = round(mb_processed, 2)
    print('Processamento estimado: {} MB'.format(mb_processed))
    


