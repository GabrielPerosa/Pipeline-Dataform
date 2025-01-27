# API Dataform

- [Documentação Dataform](https://cloud.google.com/python/docs/reference/dataform/latest/google.cloud.dataform_v1beta1.services.dataform.DataformAsyncClient#properties)


## Objetivo
Esse programa foi desenvolvido com a finalidade de testar a conexão com a API do Dataform no GCP. Usando a biblioteca do Python para datafrom, implementamos algumas logicas que manipulam o **workspace** de um repositório do Dataform.

## Implementação
Usamos as bibliotecas: `google-api-core`, `google-auth`e `google-cloud-dataform` para autenticar obtendo a chave do serviço do **Secret Manager** e enviar solicitações a API do Dataform. 
Primeiro autenticamos usando uma função que obteria as credenciais necessárias para criamos um Cliente Dataform. Com isso, podemos dar continuidade e implementar uma lógica que enviaria solicitações ao Dataform para criarmos arquivos, listarmos repositórios entre outros.

