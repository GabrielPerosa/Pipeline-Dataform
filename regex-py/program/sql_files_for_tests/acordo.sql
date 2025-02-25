  DECLARE nom_processo STRING DEFAULT "cobranca_acordo.sqlx";
  DECLARE nom_tabela STRING DEFAULT "cobranca_acordo";
  DECLARE dat_ini_movimento DATE;
  DECLARE dat_fim_movimento DATE;
  DECLARE dth_ult_data_processada TIMESTAMP;
  DECLARE dth_inicio_execucao TIMESTAMP;
  DECLARE atual_ult_data_processada TIMESTAMP;
  DECLARE before_rows_count INT64;
  DECLARE after_rows_count INT64;
  SET @@query_label = "routine:cobranca_acordo";
  CALL integracaohomologado.corp_gestao_processamento.get_processo_log(
    nom_processo,
    nom_tabela,
    dat_ini_movimento,
    dat_fim_movimento,
    dth_ult_data_processada,
    dth_inicio_execucao
  );
  SET before_rows_count = (
    SELECT
      row_count
    FROM
      ${ref("__TABLES__")}
    WHERE
      table_id = 'cobranca_acordo'
  );
}
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
    ${ref('pfs_risco_raw_tivea', 'acordo')}
  WHERE
    production_date BETWEEN dat_ini_movimento AND dat_fim_movimento
),
acordo_linha AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY id_cliente_externo, num_acordo, dat_referencia ORDER BY COALESCE(CAST(qtd_dias_atraso AS INT64), 0)
 DESC) AS rn
  FROM acordo
),
cliente AS (
    SELECT
        num_cpf_cnpj_cliente,
        id_cliente_externo,
        dat_referencia
    FROM
        ${ref('pfs_risco_tivea', 'cobranca_cliente')}
    WHERE
        dat_referencia BETWEEN dat_ini_movimento AND dat_fim_movimento
),

updatePartitionFilter
uniqueKey
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
        dat_referencia BETWEEN dat_ini_movimento AND dat_fim_movimento
),
neg AS (
    SELECT
        id AS id_acordo_cobranca,
        negociacao.nome AS nom_acordo_negociacao,
        negociacao.id AS id_acordo_negociacao,
        negociacao.modalidade.nome AS nom_modalidade_acordo,
        production_date AS dat_referencia
    FROM
        ${ref('pfs_risco_raw_tivea', 'acordo')}
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
        ${ref('pfs_risco_raw_tivea', 'acordo')}
    WHERE
        production_date BETWEEN dat_ini_movimento AND dat_fim_movimento
)
SELECT
    CAST(aco.id_acordo_cobranca AS INT64) AS id_acordo_cobranca,
    CAST(aco.id_cliente_externo AS INT64) AS id_cliente_externo,
    cli.num_cpf_cnpj_cliente,
    aco.id_cobrador,
    tip.nom_cobrador,
    neg.nom_modalidade_acordo AS tip_modalidade_acordo,
    CAST(aco.num_acordo AS INT64) AS num_acordo,
    CAST(aco.num_parcelas AS INT64) AS num_parcelas,
    CAST(aco.dat_operacao AS TIMESTAMP) AS dat_operacao,
    CAST(aco.dat_emissao AS TIMESTAMP) AS dat_emissao,
    CAST(aco.dth_processamento AS TIMESTAMP) AS dth_processamento,
    CAST(aco.dth_inclusao_origem AS TIMESTAMP) AS dth_inclusao_origem,
    CAST(aco.dth_alteracao_origem AS TIMESTAMP) AS dth_alteracao_origem,
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
    CAST(neg.id_acordo_negociacao AS INT64) AS id_acordo_negociacao,
    neg.nom_acordo_negociacao,
    tip.tip_acordo_meio_pagto,
    aco.dat_referencia
FROM
    acordo_linha aco
LEFT JOIN cliente cli ON aco.id_cliente_externo = cli.id_cliente_externo AND aco.dat_referencia = cli.dat_referencia AND aco.rn = 1
LEFT JOIN origem_acordo ori ON CAST(aco.id_acordo_cobranca AS STRING) = CAST(ori.id_acordo_cobranca AS STRING) AND aco.dat_referencia = ori.dat_referencia AND ori.rn = 1
LEFT JOIN neg neg ON aco.id_acordo_cobranca = neg.id_acordo_cobranca AND aco.dat_referencia = neg.dat_referencia
LEFT JOIN tip_pag_assess_user tip ON aco.id_acordo_cobranca = tip.id_acordo_cobranca AND aco.dat_referencia = tip.dat_referencia
WHERE aco.rn = 1
post_operations {
  SET after_rows_count = (
    SELECT
      row_count
    FROM
      ${ref("__TABLES__")}
    WHERE
      table_id = 'cobranca_acordo'
  );
  SET atual_ult_data_processada = (
    SELECT
      max(dth_processamento)
    FROM
      ${self()}
    WHERE
      dth_processamento >= dth_ult_data_processada
      AND dat_referencia BETWEEN dat_ini_movimento AND dat_fim_movimento
    LIMIT 1
  );
  CALL integracaohomologado.corp_gestao_processamento.insert_processo_log(
    nom_processo,
    nom_tabela,
    dat_ini_movimento,
    dat_fim_movimento,
    atual_ult_data_processada,
    dth_inicio_execucao,
    (
      SELECT
        after_rows_count - before_rows_count AS count
    ),
    "EXECUÇÃO FINALIZADA COM SUCESSO"
  );'