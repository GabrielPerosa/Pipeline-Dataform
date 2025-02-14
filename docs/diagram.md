```mermaid
sequenceDiagram
    participant Dev as Desenvolvedor
    participant GitHub as GitHub (staging)
    participant CloudBuild as Cloud Build
    participant SQLFluff as Validador SQLFluff
    participant GitProd as GitHub (produção)
    participant Dataform as Dataform GCP

    Dev->>GitHub: Commit e Push para staging
    GitHub->>CloudBuild: Dispara pipeline do Cloud Build
    CloudBuild->>SQLFluff: Executa SQLFluff para validar scripts
    alt Testes aprovados
        CloudBuild->>GitProd: Faz merge para produção
        CloudBuild->>Dataform: Envia scripts para o Dataform
    else Testes falharam
        CloudBuild->>Dev: Notifica erro nos scripts
    end
