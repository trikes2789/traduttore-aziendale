from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# CONFIGURAZIONE
AZURE_KEY = os.environ.get('AZURE_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
APP_PASSWORD = os.environ.get('APP_PASSWORD')

# --- NOTA: Ho cambiato il nome della funzione qui sotto da 'handler' a 'traduci_documento' ---
@app.route('/api/traduci', methods=['POST'])
def traduci_documento():
    # 1. Controllo Sicurezza (Password)
    user_pass = request.headers.get('x-app-password')
    if user_pass != APP_PASSWORD:
        return Response("Password errata/Non autorizzato", status=401)

    # 2. Controllo File
    if 'file' not in request.files:
        return Response("Nessun file caricato", status=400)
    
    file = request.files['file']
    target_lang = request.form.get('target_lang', 'it')

    # 3. Chiamata ad Azure
    url = f"{AZURE_ENDPOINT}/translator/document:translate?sourceLanguage=en&targetLanguage={target_lang}&api-version=2024-05-01"
    
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
    }

    files_payload = {
        'document': (file.filename, file.stream, 'application/pdf')
    }

    try:
        response = requests.post(url, headers=headers, files=files_payload)
        
        if response.status_code != 200:
            return Response(f"Errore Azure: {response.text}", status=500)

        return Response(
            response.content,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=tradotto.pdf"}
        )

    except Exception as e:
        return Response(str(e), status=500)

# Necessario per Vercel
if __name__ == '__main__':
    app.run()