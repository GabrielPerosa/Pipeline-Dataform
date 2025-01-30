from google.cloud import dataform_v1beta1
from googleapiclient.discovery import build
from google.cloud.dataform_v1beta1 import types
from files import load_files, get_content
from auth import get_auth
from dotenv import load_dotenv
from files import load_files, get_content
import os

load_dotenv()

# Secret 
secret = "pfs-risco-tivea-key"

# Project Vars
project_id = os.getenv('PROJECT_ID')
project_number = os.getenv('PROJECT_NUMBER')
location = os.getenv('LOCATION')
parent = f'projects/{project_id}/locations/{location}'


# Dataform vars
repository = os.getenv('REPOSITORY')
workspace_name = os.getenv('WORKSPACE_NAME')

workspace_path = f"{parent}/repositories/{repository}/workspaces/{workspace_name}"

credentials = get_auth(project_number, secret)

# cliente da API Dataform
service = dataform_v1beta1.DataformClient(credentials=credentials)
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

print(f"Arquivos enviados: {files}")