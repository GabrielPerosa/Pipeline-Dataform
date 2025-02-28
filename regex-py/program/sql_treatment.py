import re
import os

def sql_treatment(content, variables):
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

    return ready_sql

def sub_dates_in_sqlcode(file_content, dates):
    matches = re.findall(r"DECLARE\s+(\w+)\s+DATE.*?;", file_content, re.IGNORECASE)
    if(matches):
        i = 0
        for m in matches:
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
    file_content = re.sub(r"\$\{ref(.*?)}", path, file_content, count=1)

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
