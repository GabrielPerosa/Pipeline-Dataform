import os
import re
from files import get_content, load_files


dates = ['2023-01-01', '2023-12-31']
    # Obtendo conteudo
file_content = """
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
   
                    """




# Buscar tabela e dataset (name e processo) 
def get_value_of_key(key, file_content):
    
    pattern_prefix = fr'{key}:\s*\w*\s*(.*)'
    name = re.search(pattern_prefix, file_content)
    
    # Limpando string
    name = name.group(1)
    name = name.replace("'", "")
    name = name.strip()
    
    return name
    

def sub_dataset_table(file_content):
  pattern = r"\$\{ref\('([^']+)',\s*'([^']+)'\)\}"
  matches = re.search(pattern, file_content, re.IGNORECASE)

  dataset = matches.group(1)
  table = matches.group(2)

  path = "{}.{}".format(dataset, table)

  return path

def only_sql_to_bigquery(file_content):
  pattern = r"(?s)DECLARE.*?\n}"
  matches = re.search(pattern, file_content, re.IGNORECASE)
  
  text_to_remove = matches.group(0)

  # Limpando espaços vazios
  file_content = file_content.replace(text_to_remove, "")
  file_content = file_content.strip()

  return file_content

only_sql_to_bigquery(file_content)