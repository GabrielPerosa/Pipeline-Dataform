import re
import os

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

def converter_sqlx_para_bigquery(content, variables):
    """
    Converte código SQLX para SQL do BigQuery, removendo declarações de variáveis.

    Args:
        sqlx_code (str): Código SQLX de entrada.
        variaveis_valores (dict): Dicionário com nomes de variáveis e seus valores literais.

    Returns:
        str: Código SQL do BigQuery convertido.
    """

    # Remove declarações de variáveis
    lines = content.splitlines()
    cleaned_lines = [
        line for line in lines if not re.match(r"DECLARE\s+\w+(\s+DATE\s+.*)?;", line, re.IGNORECASE)
    ]
    sql_cleaned = "\n".join(cleaned_lines)

    # Substitui variáveis por valores literais
    codigo_bigquery = codigo_sem_declaracoes
    for variavel, valor in variaveis_valores.items():
        codigo_bigquery = re.sub(r"\b" + variavel + r"\b", str(valor), codigo_bigquery)

    return codigo_bigquery