
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.auth import default
'''
A função 'acess_secret' tem o objetivo de obter a secret armazenada no Secret Manager. 
Passamos a número do projeto e o id da secret para obtermnos a secret.
EX:
    service_account_json = access_secret(project_number, secret_id)
'''

def access_secret(project_number, secret_id):
    credentials, _ = google.auth.default()

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
        # Obtendo as credenciais padrão (isso já deve cuidar de renovações de tokens e autenticação)
        credentials, project = default()

        # Se for necessário, você pode adicionar algum código para verificar se o token está expirado
        if credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        print(f"Autenticação bem-sucedida para o projeto {project_number}")
        return credentials

    except exceptions.DefaultCredentialsError as e:
        print(f"Erro ao obter credenciais: {e}")
        return None
    except Exception as e:
        print(f'Erro no Auth.py: {e}')
        return None
