import re
import os

variabels_words = {
    "BETWEEN",
    "AND",
    "OR",
    "NOT",
    "IN",
    "@@query_label"
}

def search_variables(array,file):
    """
    OBJETIVO: Buscar variaveis em um arquivo de texto.
    
    PARÂMETROS: Recebe uma string como conteudo.
    """
    for word in array:
        match = re.search(fr"\b{word}\b",fil, ere.IGNORECASE)
        if match:
            print(f"Commando {word}: \033[32mOK\033[0m")
        else:
            print(f"Commando {word}: \033[31mNONE\033[0m")
    
def search_dates(file):
    """
    OBJETIVO: Buscar datas em um arquivo de texto.

    PARÂMETROS: Recebe uma string como conteudo.
    """
    dates = re.findall(r'\d{4}-\d{2}-\d{2}',file)
    if dates:
        print(f"Commando {dates}: \033[32mOK\033[0m")
    else:
        print(f"Commando {dates}: \033[31mNONE\033[0m")

def find_name(output_name, name_to_find, file):
    """
    OBJETIVO: Buscar um nome em um arquivo de texto.

    PARÂMETROS: Recebe uma string como conteudo.
    """
    pattern_prefix = fr'{name_to_find}:\s*["\']([A-Za-z0-9_]+)["\']\s*,?'
    pattern_name= fr'["\']([A-Za-z0-9_]+)["\']\s*,?'
    name = re.search(pattern_prefix, file)
    repeated = re.findall(pattern_name, file)
    
    if repeated:
        count_often = len(repeated)
        print(f"Nome da {output_name}: {name.group(1)}  REPETIÇÕES: {count_often}")
    else:
        print(f"Nome da {output_name} não encontrado.")
    
def validation_if_exists(content):
    """
    OBJETIVO:   Validar se há presença de palavra-chaves especificadas.
    
    PARÂMETROS: Recebe uma string como conteudo.
    """
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

def validate_partitionDefinition(content):
    """
    OBJETIVO: Validar se foi definida a partição da view e verificar se foi usada no código SQL.

    PARÂMETROS: o conteudo que passará por validação.
    """
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
    
def validate_create_table(content):
    """ 
    OBJETIVO: Validar se existe o comando para criar tabela se ela não existir.

    PARÂMETROS: O conteudo que passará por validação.
    """
    # Verifica se existe create table if not exists 
    create_table_pattern = r'pre_operations\s*\{\s*CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS'
    result = re.search(create_table_pattern, content, re.IGNORECASE)
    
    if (result):
        print("--> CREATE TABLE IF NOT EXISTS em pre_operations\33[33m: OK\033[0m")
    else:
        print("\033[33m--> Não há CREATE TABLE IF NOT EXISTS em pre_operations\033[0m")

def validate_type_in_config(content):
    """
    OBJETIVO: Validar se o tipo da configuração do script é incremental ou não.

    PARÂMETROS: O conteúdo que passará por validação.

    RETORNO: True se o tipo for incremental.
    """
    # Verifica se type = incremental
    incremental_pattern = r'type:\s*"([^"]+)"'
    result = re.search(incremental_pattern, content)
    return result.group(1)

def create_sql_for_validate(content, file_name):
    """
    OBJETIVO: Criar um arquivo SQL para validar se a tabela existe.

    PARâMETROS: O conteúdo que passará por validação e o nome do arquivo.
    """
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

def validate_where_clause(content):
    # Padrão regex para encontrar cláusulas WHERE com as condições especificadas
    pattern = r'(WHERE\s+[^;]*\s*(<=\s*CURRENT_DATE\(\)|<\s*CURRENT_DATE\(\)|<=\s*CURRENT_TIMESTAMP\(\))\s*[^;]*)'
    
    # Busca todas as ocorrências no conteúdo, ignorando maiúsculas/minúsculas
    matches = re.findall(pattern, content, re.IGNORECASE)
    
    # Conta o número de cláusulas encontradas
    num_matches = len(matches)
    
    # Exibe mensagem colorida no terminal
    if num_matches == 0:
        print("\033[31mNenhuma cláusula WHERE com as condições especificadas encontrada.\033[0m")
    else:
        print(f"\033[32mEncontradas {num_matches} cláusulas WHERE com as condições especificadas.\033[0m")
        # Opcional: listar as cláusulas encontradas
        for i, match in enumerate(matches, 1):
            print(f"Cláusula {i}: {match[0].strip()}")

def exec_validations(content, file_name):
    """
    OBJETIVO: centralizar e executar funções de validação. Caso haja erro, retorna uma exceção.
    
    PARÂMETROS: Recebe uma string como conteudo e outra como nome do arquivo.
    """
    try:
        print(f"Iniciando validação em: {file_name}")
        validate_where_clause(content)
        validate_partitionDefinition(content)
        validate_create_table(content)
        validation_if_exists(content)
        create_sql_for_validate(content, file_name)
        find_name("dataset","processo",content)
        find_name("tabela","name",content)
        find_name("partição","partitionBy",content)
        search_variables(variabels_words,content)
    
    except Exception as e:
        return e
