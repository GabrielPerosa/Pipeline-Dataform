import re
import os
from files import load_files, get_content
from google.cloud import bigquery

dates = ['2023-01-01', '2023-12-31']

def create_sql_for_validate(content, file_name):
    """
    OBJETIVO: Criar um arquivo SQL para validar se a tabela existe.

    PARâMETROS: O conteúdo que passará por validação e o nome do arquivo.
    """
    sql_folder = './sql_files_for_tests'

    # Padrão para encontrar código SQL
    pattern = r"pre_operations\s*{.*?post_operations$"

    # busca a incidencia no conteudo
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # obter codigo
        sql_code = match.group() 
        lines = sql_code.splitlines()

        # remove linhas desnecessárias
        sql_cleaned = '\n'.join(lines[1:-1])
            
        # Cria a pasta para armazenar SQLs
        if not os.path.exists(sql_folder):
            os.makedirs(sql_folder)

        file_name = file_name.replace("sqlx", "sql")
        path = './sql_files_for_tests/{}'.format(file_name)

        # Grava arquivo para realizar teste
        with open(path, "w", encoding="utf-8") as file:
            file.write(sql_cleaned)
            print("Gravado com Sucesso:\033[33m {} \033[0m".format(file_name))

def convert_sqlx_to_bigquery_sql(content, variables):
    """
    Converte código SQLX para SQL do BigQuery, removendo declarações de variáveis.

    Args:
        sqlx_code (str): Código SQLX de entrada.
        variaveis_valores (dict): Dicionário com nomes de variáveis e seus valores literais.

    Returns:
        str: Código SQL do BigQuery convertido.
    """
    sql_with_valid_dates = sub_dates_in_sqlcode(content, variables)
    sql_only = only_sql_to_bigquery(sql_with_valid_dates)
    cleaned_sql = sub_dataset_table(sql_only)
    ready_sql = cast_to_safe_cast(cleaned_sql)
    # Grava arquivo para realizar teste
    print(ready_sql)
    
    return ready_sql

def sub_dates_in_sqlcode(file_content, dates):
    matches = re.findall(r"DECLARE\s+(\w+)\s+DATE.*?;", file_content, re.IGNORECASE)
    if(matches):
        i = 0
        for m in matches:
            print(m)
            date_value = dates[i]
            file_content = re.sub(fr'\b{m}\b', f"CAST('{date_value}' AS DATE)", file_content)
            i+=1
    return file_content

def sub_dataset_table(file_content):
  pattern = r"\$\{ref\('([^']+)',\s*'([^']+)'\)\}"
  matches = re.findall(pattern, file_content, re.IGNORECASE)
  
  for match in matches:
    # Obtendo dataset e tabela de cada correspondência
    dataset, table = match
    path = "{}.{}".format(dataset, table)

    file_content = re.sub(r"\$\{ref(.*?)}", path, file_content)

  return file_content

def cast_to_safe_cast(content):
  pattern = r"\bCAST\b"
  content = re.sub(pattern, "SAFE_CAST", content)
  return content

def only_sql_to_bigquery(file_content):
  pattern = r"(?s)DECLARE.*?\n}"
  matches = re.search(pattern, file_content, re.IGNORECASE)
  
  text_to_remove = matches.group(0)

  # Removendo parte inútil e limpando espaços vazios 
  file_content = file_content.replace(text_to_remove, "")
  file_content = file_content.strip()

  return file_content


files, _ = load_files('./sql_files_for_tests/')
for f in files:
    content = get_content('./sql_files_for_tests/', f)
    sub_dataset_table(content)
    sql_code = convert_sqlx_to_bigquery_sql(content, dates)
    
    client = bigquery.Client(project='integracaohomologado')

    job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

    # Start the query, passing in the extra configuration.
    #query_job = client.query(str(sql_code), job_config)  # Make an API request.
    query_job = client.query((
        """
       -- Declarar variáveis (opcional, ajuste conforme necessário)
DECLARE dat_ini_movimento DATE DEFAULT '2023-01-01';
DECLARE dat_fim_movimento DATE DEFAULT '2023-12-31';

-- CTEs ajustadas
WITH acordo AS (
  SELECT
    id AS id_acordo_cobranca,
    cliente AS id_cliente_externo,
    cobrador AS id_cobrador,
    tipo AS nom_modalidade_acordo,
    numeroAcordo AS num_acordo,
    numeroParcelas AS num_parcelas,
    dataOperacao AS dat_operacao,
    dataEmissao AS dat_emissao,
    dataProcessamento AS dth_processamento,
    dataVencimento AS dat_vencimento,
    situacao AS ind_situacao,
    taxaOperacao AS val_taxa_operacao,
    valorPrincipal AS val_principal,
    valorJuros AS val_juros,
    valorPagoTributo AS val_atributo,
    valorTotal AS val_total,
    saldoPrincipal AS val_saldo_principal,
    saldoTotal AS val_saldo_total,
    saldoAtual AS val_saldo_atual,
    diasAtraso AS qtd_dias_atraso,
    production_date AS dat_referencia
  FROM
    `integracaohomologado.pfs_risco_raw_tivea.acordo`  -- Substitua pelo caminho real da tabela
  WHERE
    production_date BETWEEN dat_ini_movimento AND dat_fim_movimento
),
acordo_linha AS (
  SELECT *, 
    ROW_NUMBER() OVER (PARTITION BY id_cliente_externo, num_acordo, dat_referencia 
                       ORDER BY COALESCE(CAST(qtd_dias_atraso AS INT64), 0) DESC) AS rn
  FROM acordo
),
cliente AS (
  SELECT
    id_cliente_externo,
    production_date AS dat_referencia
  FROM
    `integracaohomologado.pfs_risco_raw_tivea.cliente`  -- Substitua pelo caminho real da tabela
  WHERE
    production_date BETWEEN dat_ini_movimento AND dat_fim_movimento
),

tip_pag_assess_user AS (
  SELECT
    id AS id_acordo_cobranca,
    meioPagamento.id AS id_acordo_pagto,
    meioPagamento.tipo AS tip_acordo_meio_pagto,
    meioPagamento.cobrador.nome AS nom_cobrador,
    assessoria.id AS id_acordo_assessoria,
    assessoria.nome AS nom_acordo_assessoria,
    usuario.id AS id_acordo_usuario,
    usuario.nome AS nom_acordo_usuario,
    production_date AS dat_referencia
  FROM
    `integracaohomologado.pfs_risco_raw_tivea.acordo`  -- Substitua pelo caminho real da tabela
  WHERE
    production_date BETWEEN dat_ini_movimento AND dat_fim_movimento
)

-- Consulta principal
SELECT
  CAST(aco.id_acordo_cobranca AS INT64) AS id_acordo_cobranca,
  CAST(aco.id_cliente_externo AS INT64) AS id_cliente_externo,
  cli.num_cpf_cnpj_cliente,
  aco.id_cobrador,
  tip.nom_cobrador,
  CAST(aco.num_acordo AS INT64) AS num_acordo,
  CAST(aco.num_parcelas AS INT64) AS num_parcelas,
  CAST(aco.dat_operacao AS TIMESTAMP) AS dat_operacao,
  CAST(aco.dat_emissao AS TIMESTAMP) AS dat_emissao,
  CAST(aco.dth_processamento AS TIMESTAMP) AS dth_processamento,
  CAST(aco.dat_vencimento AS DATE) AS dat_vencimento,
  aco.ind_situacao,
  CAST(aco.val_taxa_operacao AS INT64) AS val_taxa_operacao,
  CAST(aco.val_principal AS INT64) AS val_principal,
  CAST(aco.val_juros AS INT64) AS val_juros,
  CAST(aco.val_atributo AS INT64) AS val_atributo,
  CAST(aco.val_total AS INT64) AS val_total,
  CAST(ori.val_desconto_total AS INT64) AS val_desconto,
  CAST(aco.val_saldo_principal AS INT64) AS val_saldo_principal,
  CAST(aco.val_saldo_total AS INT64) AS val_saldo_total,
  CAST(aco.val_saldo_atual AS INT64) AS val_saldo_atual,
  CAST(aco.qtd_dias_atraso AS INT64) AS qtd_dias_atraso,
  CAST(ori.dat_atraso_orig_acordo AS DATE) AS dat_atraso_orig_acordo,
  CAST(tip.id_acordo_usuario AS INT64) AS id_acordo_usuario,
  tip.nom_acordo_usuario,
  CAST(tip.id_acordo_assessoria AS INT64) AS id_acordo_assessoria,
  tip.nom_acordo_assessoria,
  tip.tip_acordo_meio_pagto,
  aco.dat_referencia
FROM
  acordo_linha aco
LEFT JOIN cliente cli 
  ON aco.id_cliente_externo = cli.id_cliente_externo 
  AND aco.dat_referencia = cli.dat_referencia 
  AND aco.rn = 1
LEFT JOIN tip_pag_assess_user tip 
  ON aco.id_acordo_cobranca = tip.id_acordo_cobranca 
  AND aco.dat_referencia = tip.dat_referencia
WHERE
  aco.rn = 1
        """
    ), job_config)  # Make an API request.

    print(" {} bytes processados aproximadamente.".format(query_job.total_bytes_processed))

    