import re
import os
from files import load_files, get_content
from google.cloud import bigquery

dates = ['2023-01-01', '2023-12-31']

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

def convert_sqlx_to_bigquery_sql(content, variables):
    """
    Converte código SQLX para SQL do BigQuery, removendo declarações de variáveis.

    Args:
        sqlx_code (str): Código SQLX de entrada.
        variaveis_valores (dict): Dicionário com nomes de variáveis e seus valores literais.

    Returns:
        str: Código SQL do BigQuery convertido.
    """
    sql_with_valid_dates = sub_dates_in_sqlcode(content, variables)
    sql_only = only_sql_to_bigquery(sql_with_valid_dates)
    cleaned_sql = sub_dataset_table(sql_only)
    ready_sql = cast_to_safe_cast(cleaned_sql)
    # Grava arquivo para realizar teste
    print(ready_sql)
    
    return ready_sql

def sub_dates_in_sqlcode(file_content, dates):
    matches = re.findall(r"DECLARE\s+(\w+)\s+DATE.*?;", file_content, re.IGNORECASE)
    if(matches):
        i = 0
        for m in matches:
            print(m)
            date_value = dates[i]
            file_content = re.sub(fr'\b{m}\b', f"CAST('{date_value}' AS DATE)", file_content)
            i+=1
    return file_content

def sub_dataset_table(file_content):
  pattern = r"\$\{ref\('([^']+)',\s*'([^']+)'\)\}"
  matches = re.findall(pattern, file_content, re.IGNORECASE)
  
  for match in matches:
    # Obtendo dataset e tabela de cada correspondência
    dataset, table = match
    path = "{}.{}".format(dataset, table)

    file_content = re.sub(r"\$\{ref(.*?)}", path, file_content)

  return file_content

def cast_to_safe_cast(content):
  pattern = r"\bCAST\b"
  content = re.sub(pattern, "SAFE_CAST", content)
  return content

def only_sql_to_bigquery(file_content):
  pattern = r"(?s)DECLARE.*?\n}"
  matches = re.search(pattern, file_content, re.IGNORECASE)
  
  text_to_remove = matches.group(0)

  # Removendo parte inútil e limpando espaços vazios 
  file_content = file_content.replace(text_to_remove, "")
  file_content = file_content.strip()

  return file_content


files, _ = load_files('./sql_files_for_tests/')
for f in files:
    content = get_content('./sql_files_for_tests/', f)
    sub_dataset_table(content)
    sql_code = convert_sqlx_to_bigquery_sql(content, dates)
    
    client = bigquery.Client(project='integracaohomologado')

    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    # Start the query, passing in the extra configuration.
    query_job = client.query(str(sql_code), job_config)  # Make an API request.

    print(" {} bytes processados aproximadamente.".format(query_job.total_bytes_processed))

    