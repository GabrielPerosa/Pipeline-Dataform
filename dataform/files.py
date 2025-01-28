import os
'''
A função 'load_files' é usada para carregar os arquivos presentes num caminho passado como argumento, que deverá ser uma string. 
Ela retorna um array de strings contendo os nomes dos arquivos e a quantidade de arquivos presentes no array.
Ex: 
    files, size = load_files("definitions/")
    print(files)
    # files: ['acordo.sqlx', 'risco.sqlx']
'''
def load_files(source_folder):
    files = os.listdir(source_folder)
    size = len(files)
    return files, size

'''
A função 'get_content' é usada para obter o conteúdo de cada arquivo. 
Para acessá-los, é necessário passar como parâmetros o caminho relativo ao arquivo e o nome do arquivo.
Ex: 
    content = get_content(source_folder, file)
    print(content)
    # Olá mundo
'''
def get_content(source_folder, file):
    with open(f'{source_folder}{file}', 'r') as file_content:
        content = file_content.read()
        return content
    
