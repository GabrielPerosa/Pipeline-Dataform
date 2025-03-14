# Descrição do Arquivo Main

## Objetivo
Este arquivo é um script em Python responsável por realizar validações em arquivos de um diretório especificado e realizar uma avaliação de custo usando SQL para os arquivos sem erros. Ele interage com diferentes módulos e funções para carregar arquivos, obter seu conteúdo, realizar validações e avaliar o custo de processos. O script também imprime relatórios e resultados durante a execução.

## Dependências

`os` - biblioteca para interagir com o sistema operacional

`files` - pacote que contém funções necessárias para carregar arquivos e obter seu conteúdo

`validations` - pacote que contém a função que executa as validações
`sql_validation` - pacote que contém a função que realiza a validação de custo


## Fluxo do Código
1. O script começa obtendo o diretório de origem dos arquivos.
```
definitions = os.getenv("SOURCE_FOLDER")    
```

2. Em seguida, ele carrega os arquivos presentes nesse diretório.
Para cada arquivo:
O conteúdo do arquivo é recuperado.
O conteúdo é validado.
```
files, size = load_files(definitions)
print('Quantidade de arquivos: {}'.format(size))
print("{}\n".format(files))

ok = []
for file in files:
    # Obtendo conteudo
    file_content = get_content(definitions, file)

    # Validações
    result = exec_validations(file_content, file)
```

3. Se o arquivo for válido, é realizada uma avaliação de custo SQL.
```
    if (result == None):
        print("\033[31m ___ Sem erros em  {} ___\033[0m\n".format(file))
        print(" ------ ")
        print("Realizando avaliação de custo: ")
        sql_cost_validation(file_content, file)
        print(" ------ ")
```

4. Caso contrário, o erro encontrado é registrado.
```
    else:
        print("Erro em \033[33m {} \033[0m - {}\n".format(file, result))
        ok.append(result)
```