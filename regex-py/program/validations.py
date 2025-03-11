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
        match = re.search(fr"\b{word}\b", file, re.IGNORECASE)
        if match:
            print(f"Commando {word}: OK")
        else:
            print(f"Commando {word}: NONE")
    
def search_dates(file):
    """
    OBJETIVO: Buscar datas em um arquivo de texto.

    PARÂMETROS: Recebe uma string como conteudo.
    """
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', file)
    if dates:
        print(f"Commando {dates}: OK")
    else:
        print(f"Commando {dates}: NONE")

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
        print("--> Type definido para: {}".format(type_config))
        
        items = ['updatePartitionFilter', 'uniqueKey']
        for i in items:
            result = re.search(i, content)
            if (result):
                print("--> {}: OK".format(i))
            else:
                raise Exception('Erro: "{}" não encontrado no arquivo'.format(i))
    else:
        print("Type não definido como incremental: {}".format(type))

def validate_partitionDefinition(content):
    """
    OBJETIVO: Validar se foi definida a partição da view e verificar se foi usada no código SQL.

    PARÂMETROS: o conteudo que passará por validação.
    """
    # Primeira parte da validação
    requirePartitionFilter = r'requirePartitionFilter:\s*true'
    result = re.search(requirePartitionFilter, content, re.IGNORECASE)
    if (result):
        print("--> requirePartitionFilter definido como TRUE")
    else:
        raise Exception('Erro: requirePartitionFilter não foi definido como true')

    # Segunda parte da validação
    partitionBy = r'partitionBy:\s*"([^"]+)",'
    result = re.search(partitionBy, content)

    if(result):
        partition_name = result.group(1)
        print("--> partitionBy foi definido: {}".format(partition_name))
        
        partitionBy = r'PARTITION BY\s+(.*)'
        partition_name_in_sql = re.search(partitionBy, content, re.IGNORECASE)
        
        if not (result):
            print("Partição não está sendo usada no código SQL")
        elif ( 0 > partition_name_in_sql.group(1).find(partition_name)):
            print("Nome da partição está diferente no código SQL")
        else:
            print("--> Partição está sendo usada no código SQL")
    else:
        print("partitionBy não definido")
    
def validate_create_table(content):
    """ 
    OBJETIVO: Validar se existe o comando para criar tabela se ela não existir.

    PARÂMETROS: O conteudo que passará por validação.
    """
    # Verifica se existe create table if not exists 
    create_table_pattern = r'pre_operations\s*\{\s*CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS'
    result = re.search(create_table_pattern, content, re.IGNORECASE)
    
    if (result):
        print("--> CREATE TABLE IF NOT EXISTS em pre_operations: OK")
    else:
        print("--> Não há CREATE TABLE IF NOT EXISTS em pre_operations")

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

def validate_where_clause(filename, content):
    """
    OBJETIVO: Verificar a presença de cláusulas WHERE contendo as condições especificadas no script SQL.
    
    PARÂMETROS: 
        filename (str): Nome do arquivo SQL sendo analisado.
        content (str): Conteúdo do script SQL a ser analisado.
    """

    print(f"\nIniciando validação em: {filename}\n")

    conditions = ["CURRENT_DATE", "CURRENT_TIMESTAMP", "dat_fim_movimento"]
    operators = ["<=", "<"]

    found_clauses = []
    
    # Verifica todas as condições com os operadores < e <=
    for cond in conditions:
        for op in operators:
            pattern = fr'WHERE\s+(\w+)\s*{re.escape(op)}\s*{cond}\(\)?'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)

            for match in matches:
                found_clauses.append(f"Cláusula {len(found_clauses) + 1}: WHERE {match} {op} {cond}()")

    if found_clauses:
        print(f"\033[32mEncontradas {len(found_clauses)} cláusulas WHERE com as condições especificadas.\033[0m\n")
        for clause in found_clauses:
            print(f"  {clause}")
    else:
        print("\033[31mNenhuma cláusula WHERE com as condições especificadas encontrada.\033[0m\n")

    # Exemplo de erro extra (personalize conforme necessário)
    if "requirePartitionFilter" not in content:
        print(f"Erro em {filename} - Erro: requirePartitionFilter não foi definido como true\n")


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
        #validation_if_exists(content)
        find_name("dataset","processo",content)
        find_name("tabela","name",content)
        find_name("partição","partitionBy",content)
        search_variables(variabels_words,content)
    
    except Exception as e:
        return e
