<div style="text-align: justify;">

# CI/CD com Cloud Build e Dataform

![Diagrama aplicação](images/image.png)

## Ferramentas Google usadas:
* Cloud Build
* Dataform

## Visão Geral
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Esta aplicação é uma demonstração de como usar Cloud Build e Dataform para criar um pipeline de CI/CD. O pipeline é responsável por dar auto-merge entre branches e realizar deploy de uma aplicação em um ambiente de produção. Com o objetivo de qualquer um que commite na branch `feature/testes-base` seja mergeado com a branch `feaure/testes`, no caso, os scripts que forão executados e testados.

## Como funciona o pipeline?
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;O usuário faz um commit na branch `feature/testes-base`. Nela tem que ter um arquivo `cloudbuild.yaml`, onde é ele que define o pipeline de build e deploy. No nosso caso a branch `feature/testes-base` é monitorada pelo **cloud build** que caso tenha um commit novo ele irá executar o pipeline e atualizar o **dataform** automaticamente por meio de um script python.

## Configurações Cloud Build e Dataform
[Configuração Cloud Build](config/cloudbuild.md)

[Configuração Dataform](config/dataform.md)

## Código cloudbuild.yaml
```
steps:
  - id: 'git config'
    name: 'alpine/git'
    entrypoint: 'sh'
    args:
      - '-c'
      - |
        echo "Configurando credenciais do Git..."
        git config --global user.name "$_GIT_USER_NAME"
        git config --global user.email "$_GIT_USER_EMAIL"

  - id: 'clone repo'
    name: 'alpine/git'
    entrypoint: 'sh'
    args:
      - '-c'
      - |
        echo "Clonando o repositório..."
        git clone https://${_GIT_USER_NAME}:${_GIT_TOKEN}@github.com/GabrielPerosa/Pipeline-Dataform.git
        cd Pipeline-Dataform

  - id: 'check commits'
    name: 'alpine/git'
    entrypoint: 'sh'
    args:
      - '-c'
      - |
        echo "Verificando novos commits na branch $_FEATURE_NAME..."
        git checkout $_FEATURE_NAME
        git pull origin $_FEATURE_NAME
        if [ "$(git log origin/$_BRANCH_NAME..HEAD --oneline)" = "" ]; then
          echo "Nenhum novo commit encontrado na branch $_FEATURE_NAME. Finalizando o pipeline."
          exit 0
        fi
        echo "Novos commits encontrados na branch $_FEATURE_NAME."

  - id: 'merge branch'
    name: 'alpine/git'
    entrypoint: 'sh'
    args:
      - '-c'
      - |
        echo "Fazendo checkout da branch $_FEATURE_NAME..."
        git checkout $_FEATURE_NAME
        git pull
        echo "Fazendo merge da branch $_FEATURE_NAME na $_BRANCH_NAME..."
        git checkout $_BRANCH_NAME
        git pull
        git merge $_FEATURE_NAME --allow-unrelated-histories -X theirs
        echo "Push das mudanças para a branch $_BRANCH_NAME..."
        git push https://${_GIT_USER_NAME}:${_GIT_TOKEN}@github.com/GabrielPerosa/Pipeline-Dataform.git $_BRANCH_NAME

  - id: 'Usando Python para validar SQL e enviar para o dataform'
    name: 'python:latest'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        pip install sqlfluff
        sqlfluff lint .

        # Roda o dataform.py
        cd dataform/
        pip install -r requirements.txt
        pip install --upgrade pip
        python dataform.py

options:
  logging: CLOUD_LOGGING_ONLY

timeout: 210s
```
