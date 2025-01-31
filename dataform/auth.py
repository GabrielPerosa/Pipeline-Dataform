from google.cloud import secretmanager
import json
from google.auth import credentials
from google.oauth2 import service_account
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account

'''
A função 'acess_secret' tem o objetivo de obter a secret armazenada no Secret Manager. 
Passamos a número do projeto e o id da secret para obtermnos a secret.
EX:
    service_account_json = access_secret(project_number, secret_id)
'''

def access_secret(project_number, secret_id):
    credentials = google.auth.default()

    # Verifique se as credenciais estão com o token de acesso válido
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())

    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    secret_name = f"projects/{project_number}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(name=secret_name)
    secret_payload = response.payload.data.decode("UTF-8")
    return secret_payload


'''
A função 'get_auth' tem o objetivo de obter a autenticação para usarmos a API Google. 
Para ela passamos número do projeto e o id da secret para obter a secret por meio de 'access_secret' e depois realizar a autenticação.
EX:
    credentials = get_auth(project_number, secret)
'''

def get_auth(project_number, secret_id):
    try:
        service_account_json = access_secret(project_number, secret_id)

        # Convertendo o JSON da chave da conta de serviço em um dicionário
        service_account_info = json.loads(service_account_json)

        # Autenticação usando a chave da conta de serviço recuperada
        credentials = service_account.Credentials.from_service_account_info(
            service_account_info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        print(f"Autenticação bem-sucedida para o projeto {project}")

        print("Sucesso ao obter autenticação!")
        return credentials

    except Exception as e:
        print(f'Erro no Auth.py: {e}')
        return e