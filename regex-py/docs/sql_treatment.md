# Tratamentos para SQL compatível com BigQuery

Este arquivo contém funções para converter código SQLX em SQL compatível com o Google BigQuery.

## Dependências
`re` - biblioteca para regex

`os` - biblioteca para interagir com o sistema operacional

## Funções de tratamento
### sql_treatment(content, variables)

- **Descrição**: Converte código SQLX para SQL do BigQuery, removendo declarações de variáveis e outros elementos não compativeis com o BigQuery

- **Parâmetros**:
content (str): Código SQLX de entrada.
variables (dict): Dicionário com nomes de variáveis e seus valores.

- **Retorno**: String com o código SQL convertido.
- **Processo**: Substitui datas, remove DECLARE, ajusta referências e converte CAST para SAFE_CAST.

### sub_dates_in_sqlcode(file_content, dates)
- **Descrição**: Substitui variáveis DECLARE DATE por CAST com valores de data.
- **Parâmetros**:
file_content (str): Conteúdo do arquivo SQLX.
dates (list): Lista de valores de data.
- **Retorno**: Conteúdo ajustado.
- **Processo**: Usa regex para encontrar DECLARE DATE e substitui por CAST com valores fornecidos.

### sub_dataset_table(file_content)

- **Descrição**: Substitui ${ref('dataset', 'tabela')} por dataset.tabela.

- **Parâmetros**:
file_content (str): Conteúdo do arquivo SQLX.
- **Retorno**: Conteúdo ajustado.
Processo: Usa regex para identificar referências e substituir pelo formato correto.
cast_to_safe_cast(content)
- **Descrição**: Substitui CAST por SAFE_CAST no código.
Parâmetros:
content (str): Conteúdo do arquivo SQLX.
- **Retorno**: Conteúdo ajustado.
- **Processo**: Usa regex para substituir todas as ocorrências de CAST.

### only_sql_to_bigquery(file_content)
- **Descrição**: Remove bloco DECLARE até a chave de fechamento.
- **Parâmetros**:
file_content (str): Conteúdo do arquivo SQLX.
- **Retorno**: Conteúdo limpo.
- **Processo**: Remove seção DECLARE e limpa espaços em branco.