import re
import os
from files import get_content, load_files

def validation_exists(content):
    # Itens a validar
    items = ['partitionBy', 'requirePartitionFilter','@@query_label']
    
    for i in items:
        result = re.search(i, content)
        if(result):
            print("{}: OK".format(i))
        else:
            raise Exception('Erro: "{}" não encontrado no arquivo'.format(i))

# def validate_requirePartitionFilter_true(content):
#     result = re.search(i, content)

def exec_validations(content):
    try:
        validation_exists(content)
    except Exception as e:
        return e


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
            print("Houve um erro: {} - {}\n".format(file, result))
            ok.append(result)
    
    