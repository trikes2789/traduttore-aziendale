from flask import Flask, request, Response, send_file
import requests
import os

app = Flask(__name__)

# CONFIGURAZIONE
AZURE_KEY = os.environ.get('AZURE_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
APP_PASSWORD = os.environ.get('APP_PASSWORD')

# 1. NUOVA ROTTA: Serve la Home Page
@app.route('/')
def home():
    # Legge il file index.html che si trova nella stessa cartella di questo script
    return send_file('index.html')

# 2. ROTTA TRADUZIONE
@app.route('/api/traduci', methods=['POST'])
def traduci():
    # Controllo Password
    if request.headers.get('x-app-password') != APP_PASSWORD:
        return Response("Password errata", status=401)

    if 'file' not in request.files:
        return Response("Nessun file", status=400)
    
    file = request.files['file']
    target_lang = request.form.get('target_lang', 'it')

    # Chiamata Azure
    url = f"{AZURE_ENDPOINT}/translator/document:translate?sourceLanguage=en&targetLanguage={target_lang}&api-version=2024-05-01"
    headers = { "Ocp-Apim-Subscription-Key": AZURE_KEY }
    files_payload = { 'document': (file.filename, file.stream, 'application/pdf') }

    try:
        res = requests.post(url, headers=headers, files=files_payload)
        if res.status_code != 200:
            return Response(f"Errore Azure: {res.text}", status=500)
            
        return Response(
            res.content,
            mimetype="application/pdf",
            headers={"Content-Disposition": "attachment; filename=tradotto.pdf"}
        )
    except Exception as e:
        return Response(str(e), status=500)