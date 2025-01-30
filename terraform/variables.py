import os
import re

# Carregar o .env manualmente
def load_env(env_file):
    env_vars = {}
    with open(env_file, "r") as file:
        for line in file:
            # Ignorar linhas vazias ou comentários
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Separar chave e valor
            key, value = line.split("=", 1)
            env_vars[key.strip()] = value.strip()
    return env_vars

# Substituir placeholders no YAML
def replace_placeholders(yaml_file, env_vars):
    with open(yaml_file, "r") as file:
        yaml_content = file.read()

    # Substituir ${VAR} pelos valores do .env
    def replace_match(match):
        key = match.group(1)  # Captura o nome da variável (ex: GIT_TOKEN)
        return env_vars.get(key, match.group(0))  # Retorna o valor ou o placeholder original

    updated_content = re.sub(r"\${(\w+)}", replace_match, yaml_content)

    # Salvar o YAML atualizado
    with open(yaml_file, "w") as file:
        file.write(updated_content)

# Caminhos dos arquivos
env_file = ".env"
yaml_file = "cloudbuild.yaml"

# Carregar variáveis do .env
env_vars = load_env(env_file)

# Substituir variáveis no YAML
replace_placeholders(yaml_file, env_vars)

print("Arquivo YAML atualizado com sucesso!")
