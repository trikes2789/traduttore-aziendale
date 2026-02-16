from flask import Flask, request, Response, send_file
import requests
import os

app = Flask(__name__)

# --- CONFIGURAZIONE ---
AZURE_KEY = os.environ.get('AZURE_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
APP_PASSWORD = os.environ.get('APP_PASSWORD')

# --- ROTTA 1: Home Page ---
@app.route('/')
def home():
    # Serve il file HTML che si trova nella stessa cartella
    return send_file('index.html')

# --- ROTTA 2: API Traduzione ---
@app.route('/api/traduci', methods=['POST'])
def traduci():
    try:
        # 1. Controllo Password
        user_pass = request.headers.get('x-app-password')
        if user_pass != APP_PASSWORD:
            return Response("Password errata: accesso non autorizzato.", status=401)

        # 2. Controllo File
        if 'file' not in request.files:
            return Response("Nessun file caricato.", status=400)
        
        file = request.files['file']
        target_lang = request.form.get('target_lang', 'it')
        
        # Leggiamo il file in memoria per passarlo correttamente
        file_data = file.read()

        # 3. Preparazione Chiamata Azure
        # Nota: NON specifichiamo sourceLanguage, Azure lo rileva in automatico
        endpoint_clean = AZURE_ENDPOINT.rstrip('/')
        url = f"{endpoint_clean}/translator/document:translate?targetLanguage={target_lang}&api-version=2024-05-01"
        
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_KEY
        }

        # Inviamo il file rinominandolo 'source.pdf' per evitare errori di formato
        files_payload = {
            'document': ('source.pdf', file_data, 'application/pdf')
        }

        # 4. Esecuzione
        response = requests.post(url, headers=headers, files=files_payload)
        
        if response.status_code != 200:
            # Restituiamo l'errore esatto di Azure per il debug
            return Response(f"Errore Azure ({response.status_code}): {response.text}", status=500)
            
        # 5. Restituzione PDF Tradotto
        return Response(
            response.content,
            mimetype="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=tradotto_{target_lang}.pdf"}
        )

    except Exception as e:
        return Response(f"Errore interno del server: {str(e)}", status=500)

# Necessario per l'ambiente locale e Vercel
if __name__ == '__main__':
    app.run()