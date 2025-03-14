# Validação com RegEx

## Objetivo

O arquivo `validations.py` tem o objetivo de separar as funções de validação do arquivo principal `main.py`. A principal motivação para essa separação é diminuir o acoplamento e aumentar a coesão das funções de validação, o que facilita a manutenção e a escalabilidade do código.
## 
As validações são divididas em várias funções, cada uma com um propósito específico. Dessa forma, cada função de validação tem uma lógica particular e depende apenas do conteúdo externo que será analisado, tornando o código mais organizado e reutilizável.

## Dependências
`re` - biblioteca para regex

`os` - biblioteca para interagir com o sistema operacional

## Benefícios

- **Redução de Acoplamento**: Ao manter as funções de validação separadas do arquivo principal, reduzimos o acoplamento entre as diferentes partes do sistema, facilitando mudanças futuras.
- **Aumento da Coesão**: Cada função de validação possui uma única responsabilidade, o que aumenta a coesão e torna o código mais fácil de entender e testar.
- **Facilidade de Manutenção**: Com funções independentes e bem definidas, é mais simples realizar modificações, como adicionar novas validações ou corrigir bugs.


## Visão Geral

### `validations.py`
Esse exemplo de validations.py mostra a estrutura de cada validação e a utilização de `regex` para capturar ocorrências do padrão especificado:
```python
def validation_if_exists(content):    
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

    # Itens a validar
    item = '@@query_label'
    result = re.search(item, content)
    
    if(result):
        print("--> {}: \033[33mOK\033[0m".format(item))
    else:
        raise Exception('Erro: "{}" não encontrado no arquivo'.format(i))
```
Dessa maneira, conseguimos analisar o conteúdo, no nosso caso os scripts SQLX, e retornar o resultado da análise: **uma excessão ou nulo** 


Usamos também uma função como `Facade` para abstrair o acesso as métodos, já que não é necessário e nem eficiente importar todos eles para o arquivo `main.py`:

```python
def exec_validations(content, file_name):
    try:
        print("Iniciando validação em : {}".format(file_name))
        validate_partitionDefinition(content)
        validate_create_table(content)
        validation_if_exists(content)
        create_sql_for_validate(content, file_name)
    except Exception as e:
        return e
```

## Detalhamento das funções de validação
### 1. **search_variables**
- **Objetivo**: Buscar variáveis específicas em um arquivo de texto.
- **Argumentos**: 
  - `array`: lista de variáveis a serem buscadas.
  - `file`: conteúdo do arquivo onde as variáveis serão buscadas.
- **Retorno**: Nenhum.

---

### 2. **search_dates**
- **Objetivo**: Buscar datas no formato `YYYY-MM-DD` em um arquivo de texto.
- **Argumentos**: 
  - `file`: conteúdo do arquivo onde as datas serão buscadas.
- **Retorno**: Nenhum.

---

### 3. **find_name**
- **Objetivo**: Buscar um nome em um arquivo de texto e contar quantas vezes ele aparece.
- **Argumentos**: 
  - `output_name`: nome do objeto a ser procurado.
  - `name_to_find`: nome a ser procurado no arquivo.
  - `file`: conteúdo do arquivo onde o nome será procurado.
- **Retorno**: Nenhum.

---

### 4. **validation_if_exists**
- **Objetivo**: Validar se palavras-chave específicas estão presentes no conteúdo, especialmente para tipo "incremental".
- **Argumentos**: 
  - `content`: conteúdo do arquivo a ser validado.
- **Retorno**: Nenhum.

---

### 5. **validate_partitionDefinition**
- **Objetivo**: Validar se a partição da view foi definida e se está sendo usada no código SQL.
- **Argumentos**: 
  - `content`: conteúdo do arquivo a ser validado.
- **Retorno**: Nenhum

---

### 6. **validate_create_table**
- **Objetivo**: Verificar a presença de um comando `CREATE TABLE IF NOT EXISTS` em um arquivo.
- **Argumentos**: 
  - `content`: conteúdo do arquivo a ser validado.
- **Retorno**: Nenhum

---

### 7. **validate_type_in_config**
- **Objetivo**: Validar se o tipo de configuração do script é "incremental".
- **Argumentos**: 
  - `content`: conteúdo do arquivo a ser validado.
- **Retorno**: Retorna o tipo da configuração (se "incremental" ou outro).

---

### 8. **validate_where_clause**
- **Objetivo**: Verificar a presença de cláusulas WHERE específicas com condições definidas.
- **Argumentos**: 
  - `filename`: nome do arquivo sendo analisado.
  - `content`: conteúdo do arquivo SQL a ser analisado.
- **Retorno**: Nenhum.

---

### 9. **exec_validations**
- **Objetivo**: Centralizar e executar várias funções de validação no conteúdo de um arquivo.
- **Argumentos**: 
  - `content`: conteúdo do arquivo a ser validado.
  - `file_name`: nome do arquivo sendo validado.
- **Retorno**: Retorna uma exceção se houver erro, caso contrário, executa as validações e imprime os resultados.

---

Essas funções realizam diferentes validações e buscas dentro do conteúdo de arquivos, geralmente envolvendo padrões específicos, como palavras-chave, datas, nomes e comandos SQL.
