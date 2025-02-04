from google.auth import exceptions
from google.auth.transport.requests import Request
from google.auth import default

'''
A função 'get_auth' tem o objetivo de obter a autenticação para usarmos a API Google. 

EX:
    credentials = get_auth(project_number)
'''

def get_auth(project_number):
    try:
        # Obtendo credenciais padrão
        credentials, project = default()

        # Renova as credenciais
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
