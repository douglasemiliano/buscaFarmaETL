# Use a imagem oficial do Python como base
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta que a aplicação Flask vai usar
EXPOSE 5000

# Comando para executar a aplicação
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]
