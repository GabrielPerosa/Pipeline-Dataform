import re
import os
from files import load_files, get_content
from google.cloud import bigquery
from sql_treatment import sql_treatment

dates = ['2024-01-01', '2025-02-01']

def create_sql_for_validate(content, file_name):
    """
    OBJETIVO: Criar um arquivo SQL para validar se a tabela existe.

    PARâMETROS: O conteúdo que passará por validação e o nome do arquivo.
    """
    sql_folder = './sql_files_for_tests'

    # Padrão para encontrar código SQL
    pattern = r"pre_operations\s*{.*?post_operations$"

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

        # Grava arquivo para realizar teste
        with open(path, "w", encoding="utf-8") as file:
            file.write(sql_cleaned)
            print("Gravado com Sucesso:\033[33m {} \033[0m".format(file_name))

files, _ = load_files('./sql_files_for_tests/')
for f in files:
    content = get_content('./sql_files_for_tests/', f)
    sql_code = sql_treatment(content, dates)
    client = bigquery.Client(project='integracaohomologado')

    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    query_job = client.query((sql_code), job_config)
    
    mb_processed = query_job.total_bytes_processed/pow(1024,2)
    print('Processamento estimado: {} MB'.format(mb_processed))
    


