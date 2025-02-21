import os        
from validations import exec_validations
import re
from files import get_content, load_files
    
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
    try: 
        definitions = os.getenv("_SOURCE_FOLDER")    
        if (definitions != "../definitions"):
            print("Erro ao carregar variavel de ambiente")
            definitions = '../definitions'
    except:
        print(e)
    
    # Carregando arquivos
    files, size = load_files(definitions)
    print('Quantidade de arquivos: {}'.format(size))
    print("{}\n".format(files))

    ok = []
    for file in files:
        # Obtendo conteudo
        file_content = get_content(definitions, file)

        # Validações
        result = exec_validations(file_content, file)

        if (result == None):
            print("\033[31m ___ Sem erros em  {} ___\033[0m\n".format(file))
        else:
            print("Erro em \033[33m {} \033[0m - {}\n".format(file, result))
            ok.append(result)

    find_name("dataset","processo",file_content)
    find_name("tabela","name",file_content)
    partition_exist(file_content)
    find_name("partição","partitionBy",file_content)
    search_variables(variabels_words,file_content)