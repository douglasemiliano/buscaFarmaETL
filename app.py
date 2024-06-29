from flask import Flask, send_from_directory
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
FILE_URL = "https://www.gov.br/saude/pt-br/composicao/sectics/farmacia-popular/arquivos/farmacias_credenciadas_pfpb_atualizada.xlsx/@@download/file"
FILE_NAME = "farmacias_credenciadas_pfpb_atualizada.xlsx"

# Define o URL do endpoint que você quer acessar
ENDPOINT_URL = "http://127.0.0.1:5000/download"
def call_endpoint():
    response = requests.get(ENDPOINT_URL)
    print(f"Endpoint called, status code: {response.status_code}")

# Configura o agendador para executar a tarefa uma vez por mês
scheduler = BackgroundScheduler()
scheduler.add_job(func=call_endpoint, trigger="interval", weeks=4)
scheduler.start()

# Garantir que o agendador seja desligado quando a aplicação for encerrada
atexit.register(lambda: scheduler.shutdown())


@app.route('/download')
def download_file():
    response = requests.get(FILE_URL)
    file_path = os.path.join(DOWNLOAD_FOLDER, FILE_NAME)

    with open(file_path, 'wb') as file:
        file.write(response.content)

    return f"Arquivo baixado com sucesso e salvo em {file_path}"


@app.route('/get-file')
def get_file():
    return send_from_directory(DOWNLOAD_FOLDER, FILE_NAME, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
