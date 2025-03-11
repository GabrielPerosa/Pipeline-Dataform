# Validação Sintaxe SQL e custo de Processamento

O arquivo `sql_validation.py` tem o objetivo de armazenar a lógica necessária para estimar o custo em processsamento de consulta. 

## Dependências

## Dependências
`re` - biblioteca para regex

`os` - biblioteca para interagir com o sistema operacional

`files` - pacote que contém funções necessárias para carregar arquivos e obter seu conteúdo

`google.cloud` - biblioteca Google para interarir com serviços do Google Cloud

`sql_treatment` - pacote que contém a função interface para realizaar tratamentos no código SQL 

### **create_sql_for_validate**:
Tem o objetivo de criar um arquivo `.sql` que será base para realização de tratamentos para gerar um código compatível com o BigQuery.

**Argumentos**: 
- **content**: conteúdo sqlx que será **semi-tratado** para gerar um SQL base 
- **filename**:  nome do arquivo **.sqlx** que será criado

**Retorno**:
- **filename**: nome do arquivo .sql criado
- **Exceção**: caso haja algum erro, retorna uma exceção

### **sql_cost_validation**:
Chama a função acima responsável por criar um arquivo **.sql** base e, logo em seguida, chama a função que realiza tratamentos no arquivo gerado(**sql_treatment**), para assim obter um código compatível com o BigQuery. Depois desses dois passos, é aberta uma conexão com o cliente BigQuery para realizar uma estimativa de custo em processamento da consulta.


**Argumentos**: 
- **content**: conteúdo sqlx que será **semi-tratado** para gerar um SQL base com a função **create_sql_for_validate**
- **filename**:  nome do arquivo **.sqlx** que será criado

