<div style="text-align: justify;">

# API Dataform

## Objetivo
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Esse programa foi desenvolvido com a finalidade de testar a conexão com a API do Dataform no GCP. Usando a biblioteca do Python para dataform, implementamos algumas lógicas que manipulam o **workspace** de um repositório do Dataform.

## Implementação
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Usamos as bibliotecas: `google-api-core`, `google-auth`e `google-cloud-dataform` para autenticar obtendo a chave do serviço do **Secret Manager** e enviar solicitações a API do Dataform. 
Primeiro autenticamos usando uma função que obteria as credenciais padrão para criamos um Cliente Dataform. Com isso, pudemos dar continuidade e implementar uma lógica que enviaria solicitações ao repositório para criarmos arquivos presentes no Gatilho acionado por uma determinada *branch*.
A ideia principal consiste em:

1. Uma branch, no caso staging, seria responsável por receber *push* quando o analista de dados terminasse de validar o script.  
2. Ao receber push, o gatilho da branch staging executaria a *pipeline* encarregada de testar a sintaxe dos arquivos e, em seguida, abrir uma conexão com o Dataform e enviar os arquivos atualizados para uma nova *branch*, no caso *production*.

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Dessa maneira, o processo de validação seria automatizado, além de possibilitar novas implementações futuras, como envio de e-mail de confirmação, entre outros.

# Etapas
1. No primeiro **step**, baixamos dependências, como **sqlfluffly**, **google-dataform** e **google-auth**
2. Logo em seguida, executamos o código encarregado de autenticar usando credenciais padrão, abrir conexão e enviar arquivos para o workspace (que representaria a branch no dataform).
3. Ao final, uma mensagem de confirmação seria registrada nos logs da pipeline

  ![logs image](images/pipeline-logs.png)
  imagem mostrando os logs da pipeline bem-sucedida

# Link
- [Documentação Dataform](https://cloud.google.com/python/docs/reference/dataform/latest/google.cloud.dataform_v1beta1.services.dataform.DataformAsyncClient#properties)
