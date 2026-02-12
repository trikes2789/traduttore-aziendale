from flask import Flask, request, Response, send_file
import requests
import os

app = Flask(__name__)

# CONFIGURAZIONE
AZURE_KEY = os.environ.get('AZURE_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
APP_PASSWORD = os.environ.get('APP_PASSWORD')

# ROTTA HOME
@app.route('/')
def home():
    return send_file('index.html')

# ROTTA TRADUZIONE
@app.route('/api/traduci', methods=['POST'])
def traduci():
    # 1. Controllo Password
    if request.headers.get('x-app-password') != APP_PASSWORD:
        return Response("Password errata", status=401)

    # 2. Controllo File
    if 'file' not in request.files:
        return Response("Nessun file caricato", status=400)
    
    file = request.files['file']
    target_lang = request.form.get('target_lang', 'it')
    
    # --- FIX CRUCIALE: Leggiamo il file in memoria ---
    file_data = file.read()

    # 3. Costruiamo l'URL (Tolto sourceLanguage=en per usare l'auto-rilevamento)
    # Rimuoviamo eventuali doppi slash dall'endpoint se presenti
    base_url = AZURE_ENDPOINT.rstrip('/')
    url = f"{base_url}/translator/document:translate?targetLanguage={target_lang}&api-version=2024-05-01"
    
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY
    }

    # --- FIX CRUCIALE: Forziamo nome e tipo file ---
    # Inviamo il file chiamandolo sempre 'source.pdf' per evitare errori con caratteri strani nel nome originale
    files_payload = {
        'document': ('source.pdf', file_data, 'application/pdf')
    }

    try:
        # Invio ad Azure
        response = requests.post(url, headers=headers, files=files_payload)
        
        # Se c'è un errore, lo stampiamo per capire
        if response.status_code != 200:
            return Response(f"Errore Azure: {response.text}", status=500)
            
        # Restituiamo il PDF
        return Response(
            response.content,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=tradotto_{target_lang}.pdf"}
        )

    except Exception as e:
        return Response(str(e), status=500)

# Necessario per Vercel
if __name__ == '__main__':
    app.run()