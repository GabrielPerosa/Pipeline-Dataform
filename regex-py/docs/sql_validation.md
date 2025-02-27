# Validação Sintxe SQL e custo de Processamento

- Declarações de Variáveis: As linhas que começam com DECLARE foram removidas. O BigQuery não suporta declarações de variáveis da mesma forma que o SQLX.
- Chamadas de Procedimentos: As linhas que começam com CALL foram removidas. Essas chamadas são específicas do ambiente SQLX e não são compatíveis com o BigQuery padrão.
- Bloco post_operations: Todo o bloco post_operations foi removido. Esse bloco contém comandos que são executados após a consulta principal no SQLX, mas não são suportados no BigQuery padrão.

- ${ref(...) }: A função ${ref(...) } é usada no Dataform para referenciar tabelas em outros datasets ou projetos. No BigQuery, precisamos substituir essas referências pelos nomes completos das tabelas. 

- Datas Fixas: Como as variáveis dat_ini_movimento e dat_fim_movimento foram removidas, os filtros WHERE production_date BETWEEN dat_ini_movimento AND dat_fim_movimento foram substituídos por filtros com datas fixas.

- CAST e SAFE_CAST: As funções CAST e SAFE_CAST foram usadas para converter os tipos de dados das colunas, principalmente para INT64 (inteiro de 64 bits). 