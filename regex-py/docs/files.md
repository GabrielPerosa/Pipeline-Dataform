# Carregamento de Arquivos e Conteúdo

## Função `load_files`

### Objetivo

A função `load_files` é usada para carregar os arquivos presentes em um caminho especificado, que deve ser uma string representando o diretório. Ela retorna dois valores: uma lista contendo os nomes dos arquivos no diretório e a quantidade de arquivos presentes nessa lista.

### Parâmetros

- **source_folder** (string): Caminho do diretório onde os arquivos estão localizados.

### Retorno

- **files** (lista de strings): Contém os nomes dos arquivos presentes no diretório especificado.
- **size** (inteiro): Representa a quantidade de arquivos presentes no diretório.

### Exemplo de uso

```python
files, size = load_files("definitions/")
print(files)
# Saída: ['acordo.sqlx', 'risco.sqlx']
```

## Função `get_content`

### Objetivo

A função `get_content` é usada para obter o conteúdo de um arquivo específico localizado em um diretório. Ela abre o arquivo e lê seu conteúdo, retornando-o como uma string.

### Parâmetros

- **source_folder** (string): Caminho relativo do diretório onde o arquivo está localizado.
- **file** (string): Nome do arquivo a ser lido.

### Retorno

- **content** (string): Contém o conteúdo do arquivo lido.

### Exemplo de uso

```python
content = get_content(source_folder, file)
print(content)
# Saída: 'Olá mundo'
