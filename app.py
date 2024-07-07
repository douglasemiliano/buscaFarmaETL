from flask import Flask, send_from_directory
import requests
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from datetime import datetime

app = Flask(__name__)
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), 'downloads')
FILE_URL = "https://www.gov.br/saude/pt-br/composicao/sectics/farmacia-popular/arquivos/farmacias_credenciadas_pfpb_atualizada.xlsx/@@download/file"
FILE_NAME = "farmacias_credenciadas_pfpb_atualizada.xlsx"

# Define o URL do endpoint que você quer acessar
ENDPOINT_URL = "https://buscafarmaapi.onrender.com/actuator/health"
FRONT_URL = "https://buscafarma.onrender.com"
def call_endpoint():
    timestamp = datetime.now()
    response = requests.get(ENDPOINT_URL)
    responseFront = requests.get(FRONT_URL)
    print(f"Horário da chamada ao endpoint: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    if response.status_code == 200:
        # Imprimir o horário e o conteúdo da resposta
        print("Resposta do endpoint /actuator/health:")
        print("codigo", response.status_code)
        print(response.json())
    else:
        print(f"Falha ao acessar o endpoint. Status code: {response.status_code}")
        print("Mensagem de erro:", response.text)

    print("Response front: ", responseFront.status_code)


# Configura o agendador para executar a tarefa uma vez por mês
scheduler = BackgroundScheduler()
scheduler.add_job(func=call_endpoint, trigger="interval", minutes=10)
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
