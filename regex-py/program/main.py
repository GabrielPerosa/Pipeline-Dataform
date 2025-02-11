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
    
    