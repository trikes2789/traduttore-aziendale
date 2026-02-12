from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# CONFIGURAZIONE
AZURE_KEY = os.environ.get('AZURE_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
APP_PASSWORD = os.environ.get('APP_PASSWORD')

# Nota: Vercel indirizza automaticamente qui se il file si chiama api/index.py
@app.route('/api/index', methods=['POST']) 
def traduci():
    # 1. Password Check
    if request.headers.get('x-app-password') != APP_PASSWORD:
        return Response("Password errata", status=401)

    # 2. File Check
    if 'file' not in request.files:
        return Response("Nessun file", status=400)
    
    file = request.files['file']
    target_lang = request.form.get('target_lang', 'it')

    # 3. Azure Call
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