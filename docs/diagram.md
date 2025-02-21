```mermaid
sequenceDiagram
    participant Hom as Dataform Homologado
    participant GitHub as GitHub (Teste)
    participant CloudBuild as Cloud Build
    participant Validação as Validação
    participant GitProd as GitHub (Produção)
    participant Dataform as Dataform Produção
 
    note right of Hom: Validação
    Hom->>GitHub: Commit e Push 
    GitHub->>CloudBuild: Dispara pipeline 
    CloudBuild->>Validação: Executa testes
    note right of CloudBuild: Testes aprovados
    CloudBuild->>Hom: Falaha nos testes
    Validação->>GitProd: Merge manual
    GitProd->>Dataform: Script validados

    
```
