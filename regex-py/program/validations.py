import re
import os

"""
    OBJETIVO:   Validar se há presença de palavra-chaves especificadas
    
    PARÂMETROS: Recebe uma string como conteudo e outra 
                como nome do arquivo que serão usados para
                verificar ocorrências
    Ex:
        validation_if_exists(content)
"""
def validation_if_exists(content):    
    # type do script
    type_config =  validate_type_in_config(content)
    
    if (type_config == 'incremental'):
        print("--> Type definido para: \33[33m{}\33[0m".format(type_config))
        
        items = ['updatePartitionFilter', 'uniqueKey']
        for i in items:
            result = re.search(i, content)
            if (result):
                print("--> {}: \033[33mOK\033[0m".format(i))
            else:
                raise Exception('Erro: "{}" não encontrado no arquivo'.format(i))
    else:
        print("\33[33mType não definido como incremental:{}\33[0m".format(type))

    # Itens a validar
    item = '@@query_label'
    result = re.search(item, content)
    
    if(result):
        print("--> {}: \033[33mOK\033[0m".format(item))
    else:
        raise Exception('Erro: "{}" não encontrado no arquivo'.format(i))

"""
    OBJETIVO: Validar se foi definida a partição da view e verificar se foi usada no código SQL
    PARÂMETROS: o conteudo que passará por validação
    Ex: 
        validate_partitionDefinition(content)
        
"""
def validate_partitionDefinition(content):
    # Primeira parte da validação
    requirePartitionFilter = r'requirePartitionFilter:\s*true'
    result = re.search(requirePartitionFilter, content, re.IGNORECASE)
    if (result):
        print("--> requirePartitionFilter definido como \033[33mTRUE\033[0m")
    else:
        raise Exception('Erro: requirePartitionFilter não foi definido como true')

    # Segunda parte da validação
    partitionBy = r'partitionBy:\s*"([^"]+)",'
    result = re.search(partitionBy, content)

    if(result):
        partition_name = result.group(1)
        print("--> partitionBy foi definido: \033[33m{} \033[0m ".format(partition_name))
        
        partitionBy = r'PARTITION BY\s+(.*)'
        partition_name_in_sql = re.search(partitionBy, content, re.IGNORECASE)
        
        if not (result):
            print("\033[33mPartição não está sendo usada no código SQL\033[0m")
        elif ( 0 > partition_name_in_sql.group(1).find(partition_name)):
            print("\033[33mNome da partição está diferente no código SQL\033[0m")
        else:
            print("--> Partição está sendo usada no código SQL")
    else:
        print("\033[33mpartitionBy não definido\033[0m")
    
""" 
    OBJETIVO: Validar se existe o comando para criar tabela se ela não existir
    PARÂMETROS: O conteudo que passará por validação
    Ex: 
        validate_create_table(content)
"""
def validate_create_table(content):
    # Verifica se existe create table if not exists 
    create_table_pattern = r'pre_operations\s*\{\s*CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS'
    result = re.search(create_table_pattern, content, re.IGNORECASE)
    
    if (result):
        print("--> CREATE TABLE IF NOT EXISTS em pre_operations\33[33m: OK\033[0m")
    else:
        print("\033[33m--> Não há CREATE TABLE IF NOT EXISTS em pre_operations\033[0m")

"""
    OBJETIVO: Validar se o tipo da configuração do script é incremental ou não 
    PARÂMETROS: O conteúdo que passará por validação
    Ex: 
        validate_type_in_config(content)
"""
def validate_type_in_config(content):
    # Verifica se type = incremental
    incremental_pattern = r'type:\s*"([^"]+)"'
    result = re.search(incremental_pattern, content)
    return result.group(1)

"""
    OBJETIVO: criar arquivos .sql que serão avaliados pelo SQL Fluff na pipeline
    PARÂMETROS: Recebe uma string como conteudo e outra 
                como nome do arquivo que serão usados para
                criar o arquivo
    Ex:
        create_sql_for_validate(content, file_name)
"""

def create_sql_for_validate(content, file_name):
    sql_folder = './sql_files_for_tests'

    # Padrão para encontrar código SQL
    pattern = r"pre_operations\s*{.*?}$"

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

"""
    OBJETIVO: Verificar a presença de cláusulas WHERE que contenham a condição '<= CURRENT_DATE()' no script SQL.
    PARÂMETROS:
        content (str): Conteúdo do script SQL a ser analisado.
    Ex:
        validate_where_clause(conteudo_script)
"""

def validate_where_clause(content):
    where_pattern = r'WHERE\s+([^;]*\s*<=\s*CURRENT_DATE\(\)\s*[^;]*)'
    where_matches = re.findall(where_pattern, content, re.IGNORECASE)
    
    if not where_matches:
        print("\033[33m--> Nenhuma cláusula WHERE <= CURRENT_DATE encontrada no script\033[0m")
        return
    
    print(f"--> Cláusulas WHERE <= CURRENT_DATE encontradas: \033[33m{len(where_matches)}\033[0m")
    

"""
    OBJETIVO: Verificar a presença de cláusulas WHERE que contenham a condição '< CURRENT_DATE()' no script SQL.
    PARÂMETROS:
        content (str): Conteúdo do script SQL a ser analisado.
    Ex:
        validate_where_clause2(conteudo_script)
"""

def validate_where_clause2(content):
    where_pattern = r'WHERE\s+([^;]*\s*<\s*CURRENT_DATE\(\)\s*[^;]*)'
    where_matches = re.findall(where_pattern, content, re.IGNORECASE)
    
    if not where_matches:
        print("\033[33m--> Nenhuma cláusula WHERE < CURRENT_DATE encontrada no script\033[0m")
        return
    
    print(f"--> Cláusulas WHERE < CURRENT_DATE encontradas: \033[33m{len(where_matches)}\033[0m")


"""
    OBJETIVO: Verificar a presença de cláusulas WHERE que contenham a condição '<= CURRENT_TIMESTAMP()' no script SQL.
    PARÂMETROS:
        content (str): Conteúdo do script SQL a ser analisado.
    Ex:
        validate_where_clause3(conteudo_script)
"""

def validate_where_clause3(content):
    where_pattern = r'WHERE\s+([^;]*\s*<=\s*CURRENT_TIMESTAMP()\(\)\s*[^;]*)'
    where_matches = re.findall(where_pattern, content, re.IGNORECASE)
    
    if not where_matches:
        print("\033[33m--> Nenhuma cláusula WHERE <= CURRENT_TIMESTAMP() encontrada no script\033[0m")
        return
    
    print(f"--> Cláusulas WHERE <= CURRENT_TIMESTAMP() encontradas: \033[33m{len(where_matches)}\033[0m")



"""
    OBJETIVO: centralizar e executar funções de validação. Caso haja erro, retorna uma exceção
    PARÂMETROS: Recebe uma string como conteudo e outra como nome do arquivo
    Ex:
        result = exec_validations(content, file_name)
"""
def exec_validations(content, file_name):
    try:
        print(f"Iniciando validação em: {file_name}")
        validate_where_clause(content)
        validate_where_clause2(content)
        validate_where_clause3(content)
        validate_partitionDefinition(content)
        validate_create_table(content)
        validation_if_exists(content)
        create_sql_for_validate(content, file_name)
    except Exception as e:
        return e
