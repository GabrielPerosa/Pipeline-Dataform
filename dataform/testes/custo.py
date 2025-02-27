from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

job_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=False)

# Start the query, passing in the extra configuration.
query_job = client.query(
    (
    """
WITH
  acordo AS (
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
      dataHoraInclusao AS dth_inclusao_origem,
      dataHoraModificacao AS dth_alteracao_origem,
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
      pfs_risco_raw_tivea.acordo
    WHERE
      production_date BETWEEN '2023-01-01' AND '2023-12-31' -- Substitua pelas datas desejadas
  ),
  acordo_linha AS (
    SELECT
      *,
      ROW_NUMBER() OVER (PARTITION BY id_cliente_externo, num_acordo, dat_referencia ORDER BY COALESCE(CAST(qtd_dias_atraso AS INT64), 0) DESC) AS rn
    FROM
      acordo
  ),
  cliente AS (
    SELECT
      num_cpf_cnpj_cliente,
      id_cliente_externo,
      dat_referencia
    FROM
      pfs_risco_tivea.cobranca_cliente
    WHERE
      dat_referencia BETWEEN '2023-01-01' AND '2023-12-31' -- Substitua pelas datas desejadas
  ),
  origem_acordo AS (
    SELECT
      dat_referencia,
      id_acordo_cobranca,
      dat_vencimento AS dat_atraso_orig_acordo,
      COALESCE(CAST(val_desconto_total AS INT64), 0) + COALESCE(CAST(val_desc_permanencia AS INT64), 0) AS val_desconto_total,
      ROW_NUMBER() OVER (PARTITION BY id_acordo_cobranca, dat_referencia ORDER BY num_ordem_contrato DESC) AS rn
    FROM
      integracaohomologado.pfs_risco_tivea.cobranca_origem_acordo
    WHERE
      dat_referencia BETWEEN '2023-01-01' AND '2023-12-31' -- Substitua pelas datas desejadas
  ),
  neg AS (
    SELECT
      id AS id_acordo_cobranca,
      negociacao.nome AS nom_acordo_negociacao,
      negociacao.id AS id_acordo_negociacao,
      negociacao.modalidade.nome AS nom_modalidade_acordo,
      production_date AS dat_referencia
    FROM
      pfs_risco_raw_tivea.acordo
    WHERE
      production_date BETWEEN '2023-01-01' AND '2023-12-31' -- Substitua pelas datas desejadas
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
      pfs_risco_raw_tivea.acordo
    WHERE
      production_date BETWEEN '2023-01-01' AND '2023-12-31' -- Substitua pelas datas desejadas
  )
SELECT
  SAFE_CAST(aco.id_acordo_cobranca AS INT64) AS id_acordo_cobranca,
  SAFE_CAST(aco.id_cliente_externo AS INT64) AS id_cliente_externo,
  cli.num_cpf_cnpj_cliente,
  aco.id_cobrador,
  tip.nom_cobrador,
  neg.nom_modalidade_acordo AS tip_modalidade_acordo,
  SAFE_CAST(aco.num_acordo AS INT64) AS num_acordo,
  SAFE_CAST(aco.num_parcelas AS INT64) AS num_parcelas,
  CAST(aco.dat_operacao AS TIMESTAMP) AS dat_operacao,
  CAST(aco.dat_emissao AS TIMESTAMP) AS dat_emissao,
  CAST(aco.dth_processamento AS TIMESTAMP) AS dth_processamento,
  CAST(aco.dth_inclusao_origem AS TIMESTAMP) AS dth_inclusao_origem,
  CAST(aco.dth_alteracao_origem AS TIMESTAMP) AS dth_alteracao_origem,
  CAST(aco.dat_vencimento AS DATE) AS dat_vencimento,
  aco.ind_situacao,
  SAFE_CAST(aco.val_taxa_operacao AS INT64) AS val_taxa_operacao,
  SAFE_CAST(aco.val_principal AS INT64) AS val_principal,
  SAFE_CAST(aco.val_juros AS INT64) AS val_juros,
  SAFE_CAST(aco.val_atributo AS INT64) AS val_atributo,
  SAFE_CAST(aco.val_total AS INT64) AS val_total,
  SAFE_CAST(ori.val_desconto_total AS INT64) AS val_desconto,
  SAFE_CAST(aco.val_saldo_principal AS INT64) AS val_saldo_principal,
  SAFE_CAST(aco.val_saldo_total AS INT64) AS val_saldo_total,
  SAFE_CAST(aco.val_saldo_atual AS INT64) AS val_saldo_atual,
  SAFE_CAST(aco.qtd_dias_atraso AS INT64) AS qtd_dias_atraso,
  CAST(ori.dat_atraso_orig_acordo AS DATE) AS dat_atraso_orig_acordo,
  SAFE_CAST(tip.id_acordo_usuario AS INT64) AS id_acordo_usuario,
  tip.nom_acordo_usuario,
  SAFE_CAST(tip.id_acordo_assessoria AS INT64) AS id_acordo_assessoria,
  tip.nom_acordo_assessoria,
  SAFE_CAST(neg.id_acordo_negociacao AS INT64) AS id_acordo_negociacao,
  neg.nom_acordo_negociacao,
  tip.tip_acordo_meio_pagto,
  aco.dat_referencia
FROM
  acordo_linha aco
LEFT JOIN
  cliente cli ON aco.id_cliente_externo = cli.id_cliente_externo AND aco.dat_referencia = cli.dat_referencia AND aco.rn = 1
LEFT JOIN
  origem_acordo ori ON CAST(aco.id_acordo_cobranca AS STRING) = CAST(ori.id_acordo_cobranca AS STRING) AND aco.dat_referencia = ori.dat_referencia AND ori.rn = 1
LEFT JOIN
  neg neg ON aco.id_acordo_cobranca = neg.id_acordo_cobranca AND aco.dat_referencia = neg.dat_referencia
LEFT JOIN
  tip_pag_assess_user tip ON aco.id_acordo_cobranca = tip.id_acordo_cobranca AND aco.dat_referencia = tip.dat_referencia
    """
    ),
    job_config=job_config,
)  # Make an API request.

# A dry run query completes immediately.
print("This query will process {} bytes.".format(query_job.total_bytes_processed))