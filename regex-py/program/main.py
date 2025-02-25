import os        
from validations import exec_validations
import re
from files import get_content, load_files

if __name__ == "__main__":
    # Carregando diretório Definitions
    definitions = os.getenv("SOURCE_FOLDER")    
    
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