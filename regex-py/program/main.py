import re
import os
from files import get_content, load_files

def validation_exists(content):
    # Itens a validar
    items = ['partitionBy','requirePartitionFilter', '@@query_label']
    
    for i in items:
        result = re.search(i, content)
        if(result):
            print(" -> {}: OK".format(i))
        else:
            raise Exception('Erro: "{}" não encontrado no arquivo'.format(i))

def validate_requirePartitionFilter_true(content):
    exp = "requirePartitionFilter"
    result = re.search(r'requirePartitionFilter:\s*true', content, re.IGNORECASE)
    if (result):
        print("requirePartitionFilter definido como true")
    else:
        raise Exception('Erro: requirePartitionFilter não foi definido como true')

def validate_sql_command(content):
    # Define padrão
    pattern = r"pre_operations\s*{.*?}$"

    # busca a incidencia no conteudo
    match = re.search(pattern, content, re.DOTALL)

    # Processa o conteudo obtido
    if match:
        # obter codigo
        sql_code = match.group() 
        lines = sql_code.splitlines()

        # remove linhas desnecessárias
        sql_cleaned = '\n'.join(lines[1:-1])
            
        # Grava arquivo para realizar teste
        with open("test.sql", "w", encoding="utf-8") as file:
            file.write(sql_cleaned)
            print("Gravado com sucesso")    
        

def exec_validations(content):
    try:
        validation_exists(content)
        validate_requirePartitionFilter_true(content)
        validate_sql_command(content)
    except Exception as e:
        return e
    
variabels_words = {
    "BETWEEN",
    "AND",
    "OR",
    "NOT",
    "IN"
}

def search_variables(array,file):
    for word in array:
        match = re.search(fr"\b{word}\b",file)
        if match:
            print(f"Commando {word}: \033[32mOK\033[0m")
        else:
            print(f"Commando {word}: \033[31mNONE\033[0m")
    
def search_dates(file): 
    dates = re.findall(r'\d{4}-\d{2}-\d{2}',file)
    if dates:
        print(f"Commando {dates}: \033[32mOK\033[0m")
    else:
        print(f"Commando {dates}: \033[31mNONE\033[0m")

def find_name(output_name, name_to_find, file):
    pattern_prefix = fr'{name_to_find}:\s*["\']([A-Za-z0-9_]+)["\']\s*,?'
    pattern_name= fr'["\']([A-Za-z0-9_]+)["\']\s*,?'
    name = re.search(pattern_prefix, file)
    repeated = re.findall(pattern_name, file)
    
    if repeated:
        count_often = len(repeated)
        print(f"Nome da {output_name}: {name.group(1)}  REPETIÇÕES: {count_often}")
    else:
        print(f"Nome da {output_name} não encontrado.")


def partition_exist(file):
    partition = re.search(r'partitionBy:\s*["\']([A-Za-z0-9_]+)["\']\s*,?',file)

    if partition:
        print(f"Partição de dados: \033[32mTRUE\033[0m")
    else:
        print(f"Partição de dados: \033[31mFALSE\033[0m")


if __name__ == "__main__":
    # Carregando diretório Definitions
    definitions = os.getenv("SOURCE_FOLDER")
    print(definitions)
    
    # Carregando arquivos
    files, size = load_files(definitions)
    print('Quantidade de arquivos: {}'.format(size))
    print(files)

    ok = []
    for file in files:
        # Obtendo conteudo
        file_content = get_content(definitions, file)

        # Validações
        result = exec_validations(file_content)

        if (result == None):
            print("Não houve erros: {}\n".format(file))
        else:
            print("Houve um erro em: {} - {}\n".format(file, result))
            ok.append(result)

    find_name("dataset","processo",file_content)
    find_name("tabela","name",file_content)
    partition_exist(file_content)
    find_name("partição","partitionBy",file_content)
    search_variables(variabels_words,file_content)