# CI/CD com Cloud Build e Dataform

![Diagrama aplicação](images/image.png)

## Ferramentas Google usadas:
* Cloud Build
* Dataform

## Visão Geral
Esta aplicação é uma demonstração de como usar Cloud Build e Dataform para criar um pipeline de CI/CD. O pipeline é responsável por dar auto-merge entre branches e realizar deploy de uma aplicação em um ambiente de produção. Com o objetivo de qualquer um que commite na branch `feature/testes-base` seja mergeado com a branch `feaure/testes`, no caso, os scripts que forão executados e testados.

## Como funciona o pipeline?
O usuário faz um commit na branch `feature/testes-base`. Nela tem que ter um arquivo `cloudbuild.yaml`, onde é ele que define o pipeline de build e deploy. No nosso caso a branch `feature/testes-base` é monitorada pelo cloud build que caso tenha um commit novo ele irá executar o pipeline e atualizar o dataform automaticamente por meio de um script python.

## Código Cloud Build
````

```