# Validação com RegEx

O arquivo `validations.py` tem o objetivo de separar as funções de validação do arquivo principal `main.py`. A principal motivação para essa separação é diminuir o acoplamento e aumentar a coesão das funções de validação, o que facilita a manutenção e a escalabilidade do código.

## Objetivo

As validações são divididas em várias funções, cada uma com um propósito específico. Dessa forma, cada função de validação tem uma lógica particular e depende apenas do conteúdo externo que será analisado, tornando o código mais organizado e reutilizável.

## Benefícios

- **Redução de Acoplamento**: Ao manter as funções de validação separadas do arquivo principal, reduzimos o acoplamento entre as diferentes partes do sistema, facilitando mudanças futuras.
- **Aumento da Coesão**: Cada função de validação possui uma única responsabilidade, o que aumenta a coesão e torna o código mais fácil de entender e testar.
- **Facilidade de Manutenção**: Com funções independentes e bem definidas, é mais simples realizar modificações, como adicionar novas validações ou corrigir bugs.

## Exemplo de Estrutura

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