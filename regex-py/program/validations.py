import re
import os

"""
    OBJETIVO: validar se há presença de palavra-chave
    PARÂMETROS: Recebe uma string como conteudo e outra 
                como nome do arquivo que serão usados para
                verificar ocorrências e notificar o nome do arquivo verificado
    Ex:
        validation_exists(content, file_name)
"""
def validation_exists(content, file_name):
    # Itens a validar
    items = ['requirePartitionFilter', '@@query_label']
    
    for i in items:
        result = re.search(i, content)
        if(result):
            print(" -> {}: \033[33mOK\033[0m".format(i))
        else:
            raise Exception('Erro: "{}" não encontrado no arquivo'.format(i))

"""
    OBJETIVO: validar se há presença de palavra-chave e se foi definida como TRUE
    PARÂMETROS: Recebe uma string como conteudo usada para
                verificar ocorrência e validar se está definida como TRUE
    Ex:
        validate_requirePartitionFilter_true(content)
"""

"""
"""
def validate_partitionDefinition(content):
    # Primeira parte da validação
    requirePartitionFilter = r'requirePartitionFilter:\s*true'
    result = re.search(requirePartitionFilter, content, re.IGNORECASE)
    if (result):
        print(" -> requirePartitionFilter definido como \033[33mTRUE\033[0m")
    else:
        raise Exception('Erro: requirePartitionFilter não foi definido como true')

    # Segunda parte da validação
    partitionBy = r'partitionBy:\s*"([^"]+)",'
    partition_name = re.search(partitionBy, content)

    if(partition_name):
        print(" -> partitionBy foi definido: \033[33m{} \033[0m ".format(partition_name.group(1)))
        partitionBy = r"PARTITION BY\s+(.*)"
        partition_name_in_sql = re.search(partitionBy, content, re.IGNORECASE)

        if not (partition_name_in_sql):
            print("Partição não está sendo usada no código SQL")
        elif (partition_name.group(1) != partition_name_in_sql.group(1)):
            print("Nome na partição está diferente no código SQL")
        else:
            print("Nome da partição está presente no código SQL")
    else:
        print(" -> partitionBy não definido")
    

#def validate_type_of_incremental(content):
#    result = re.search(r'type:\s*"incremental"', content, re.IGNORECASE)
#

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
    OBJETIVO: centralizar e executar funções de validação. Caso haja erro, retorna uma exceção
    PARÂMETROS: Recebe uma string como conteudo e outra como nome do arquivo
    Ex:
        result = exec_validations(content, file_name)
"""
def exec_validations(content, file_name):
    try:
        print("Iniciando validação em : {}".format(file_name))
        validation_exists(content, file_name)
        validate_partitionDefinition(content)
        create_sql_for_validate(content, file_name)
    except Exception as e:
        return e
