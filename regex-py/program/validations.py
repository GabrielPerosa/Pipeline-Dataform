import re
import os

def validation_if_exists(content):    
    type_config = validate_type_in_config(content)
    
    if type_config == 'incremental':
        print(f"--> Type definido para: \33[33m{type_config}\33[0m")
        items = ['updatePartitionFilter', 'uniqueKey']
        for i in items:
            result = re.search(i, content)
            if result:
                print(f"--> {i}: \033[33mOK\033[0m")
            else:
                raise Exception(f'Erro: "{i}" não encontrado no arquivo')
    else:
        print(f"\33[33mType não definido como incremental: {type_config}\33[0m")

    item = '@@query_label'
    result = re.search(item, content)
    if result:
        print(f"--> {item}: \033[33mOK\033[0m")
    else:
        raise Exception(f'Erro: "{item}" não encontrado no arquivo')

def validate_partitionDefinition(content):
    requirePartitionFilter = r'requirePartitionFilter:\s*true'
    result = re.search(requirePartitionFilter, content, re.IGNORECASE)
    if result:
        print("--> requirePartitionFilter definido como \033[33mTRUE\033[0m")
    else:
        raise Exception('Erro: requirePartitionFilter não foi definido como true')

    partitionBy = r'partitionBy:\s*"([^"]+)",'
    result = re.search(partitionBy, content)
    if result:
        partition_name = result.group(1)
        print(f"--> partitionBy foi definido: \033[33m{partition_name}\033[0m")
        
        partitionBy_sql = r'PARTITION BY\s+(.*)'
        partition_name_in_sql = re.search(partitionBy_sql, content, re.IGNORECASE)
        if not partition_name_in_sql:
            print("\033[33mPartição não está sendo usada no código SQL\033[0m")
        elif partition_name_in_sql.group(1).find(partition_name) < 0:
            print("\033[33mNome da partição está diferente no código SQL\033[0m")
        else:
            print("--> Partição está sendo usada no código SQL")
    else:
        print("\033[33mpartitionBy não definido\033[0m")

def validate_create_table(content):
    create_table_pattern = r'pre_operations\s*\{\s*CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS'
    result = re.search(create_table_pattern, content, re.IGNORECASE)
    if result:
        print("--> CREATE TABLE IF NOT EXISTS em pre_operations\33[33m: OK\033[0m")
    else:
        print("\033[33m--> Não há CREATE TABLE IF NOT EXISTS em pre_operations\033[0m")

def validate_type_in_config(content):
    incremental_pattern = r'type:\s*"([^"]+)"'
    result = re.search(incremental_pattern, content)
    if result:
        return result.group(1)
    raise Exception("Erro: 'type' não definido no arquivo")

def create_sql_for_validate(content, file_name):
    sql_folder = './sql_files_for_tests'
    pattern = r"pre_operations\s*{.*?}$"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        sql_code = match.group()
        lines = sql_code.splitlines()
        sql_cleaned = '\n'.join(lines[1:-1])
        
        if not os.path.exists(sql_folder):
            os.makedirs(sql_folder)
        
        file_name = file_name.replace("sqlx", "sql")
        path = f'./sql_files_for_tests/{file_name}'
        with open(path, "w", encoding="utf-8") as file:
            file.write(sql_cleaned)
            print(f"Gravado com Sucesso:\033[33m {file_name} \033[0m")


def validate_where_clause(content):
    where_pattern = r'WHERE\s+([^;]*\s*<=\s*CURRENT_DATE\(\)\s*[^;]*)'
    where_matches = re.findall(where_pattern, content, re.IGNORECASE)
    
    if not where_matches:
        print("\033[33m--> Nenhuma cláusula WHERE <= CURRENT_DATE encontrada no script\033[0m")
        return
    
    print(f"--> Cláusulas WHERE <= CURRENT_DATE encontradas: \033[33m{len(where_matches)}\033[0m")
    
    
def validate_where_clause2(content):
    where_pattern = r'WHERE\s+([^;]*\s*<\s*CURRENT_DATE\(\)\s*[^;]*)'
    where_matches = re.findall(where_pattern, content, re.IGNORECASE)
    
    if not where_matches:
        print("\033[33m--> Nenhuma cláusula WHERE < CURRENT_DATE encontrada no script\033[0m")
        return
    
    print(f"--> Cláusulas WHERE < CURRENT_DATE encontradas: \033[33m{len(where_matches)}\033[0m")


def validate_where_clause3(content):
    where_pattern = r'WHERE\s+([^;]*\s*<=\s*CURRENT_TIMESTAMP()\(\)\s*[^;]*)'
    where_matches = re.findall(where_pattern, content, re.IGNORECASE)
    
    if not where_matches:
        print("\033[33m--> Nenhuma cláusula WHERE <= CURRENT_TIMESTAMP() encontrada no script\033[0m")
        return
    
    print(f"--> Cláusulas WHERE <= CURRENT_TIMESTAMP() encontradas: \033[33m{len(where_matches)}\033[0m")



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

