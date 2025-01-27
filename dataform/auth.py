from google.cloud import secretmanager
import json
from google.auth import credentials
from google.oauth2 import service_account

def access_secret(project_number, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_number}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=secret_name)
    secret_payload = response.payload.data.decode("UTF-8")
    return secret_payload

def getAuth(project_number, secret_id):
    try:
        service_account_json = access_secret(project_number, secret_id)

        # Convertendo o JSON da chave da conta de serviço em um dicionário
        service_account_info = json.loads(service_account_json)

        # Autenticação usando a chave da conta de serviço recuperada
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        print("Sucesso ao obter autenticação!")
        return credentials

    except Exception as e:
        print(f'Erro: {e}')
        return e