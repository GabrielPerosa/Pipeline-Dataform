from google.cloud import dataform_v1beta1
from googleapiclient.discovery import build
from google.cloud.dataform_v1beta1 import types
from dotenv import dotenv_values
from files import load_files, get_content
from auth import get_auth

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

print()

credentials = get_auth(project_number, secret)

# cliente da API Dataform
service = dataform_v1beta1.DataformClient()

# Load Files
source_folder = "../definitions/"

files, size = load_files(source_folder)
i = 0

for file in files:
    file_content = get_content(source_folder, file)
    file_content = file_content.encode("utf-8")

    request = dataform_v1beta1.WriteFileRequest(
        workspace=workspace_path,
        path=f'definitions/{file}',
        contents=file_content,
    )

try:
    result = service.write_file(request)
    print(result)
    i+=1
except Exception as e:
    print(f'Erro: {e}')
if i == 0:
    print(f'Envio fracassou: {i}/{size}')
elif i < size:
    print(f'Envio parcial: {i}/{size}')
else:
    print(f'Envio realizado com sucesso: {i}/{size}')