from google.cloud import dataform_v1beta1
from googleapiclient.discovery import build
from google.cloud.dataform_v1beta1 import types
from dotenv import dotenv_values
from auth import getAuth

config = dotenv_values(".env")

# Secret 
secret = config["SERVICE_ACCOUNT_KEY"]
# Project Vars
project_id = config["PROJECT_ID"]
project_number =config["PROJECT_NUMBER"]
location = config["LOCATION"]
parent = f'projects/{project_id}/locations/{location}'

# Dataform vars
repository = config["REPOSITORY"]
workspace_name = config["WORKSPACE_NAME"]
workspace_path = f"{parent}/repositories/{repository}/workspaces/{workspace_name}"

print(repository)
print(workspace_name)

credentials = getAuth(project_number, secret)

# cliente da API Dataform
service = dataform_v1beta1.DataformClient()

file_name = input("Digite o nome do arquivo \n")
file_name = f'{file_name}.sqlx'

file_content = input("Digite um comando sql \n")
file_content = file_content.encode("utf-8")

request = dataform_v1beta1.WriteFileRequest(
    workspace=workspace_path,
    path=file_name,
    contents=file_content,
)

try:
    result = service.write_file(request)
    print(result)
except Exception as e:
    print(f'Erro: {e}')
