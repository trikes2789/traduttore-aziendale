from flask import Flask, request, Response, send_file
import requests
import os
import io

app = Flask(__name__)

# --- CONFIGURAZIONE ---
AZURE_KEY = os.environ.get('AZURE_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT')
APP_PASSWORD = os.environ.get('APP_PASSWORD')

# --- ROTTA 1: Home Page ---
@app.route('/')
def home():
    # Cerca il file index.html nella stessa cartella (api/)
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'index.html')):
         return send_file(os.path.join(os.path.dirname(__file__), 'index.html'))
    # Fallback se è nella root (per sicurezza)
    return send_file('../index.html')

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
        
        # --- PIANO B: Lettura sicura del file ---
        # Leggiamo tutti i byte del file in memoria
        file_content = file.read()
        
        # Se il file è vuoto, fermiamo subito
        if len(file_content) == 0:
            return Response("Il file inviato è vuoto.", status=400)

        # 3. Preparazione URL Azure
        # Rimuoviamo slash finali per evitare doppi slash (es. .com//translator)
        base_url = AZURE_ENDPOINT.rstrip('/')
        url = f"{base_url}/translator/document:translate?targetLanguage={target_lang}&api-version=2024-05-01"
        
        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_KEY
            # NOTA: Non mettiamo 'Content-Type': 'multipart/form-data' qui.
            # La libreria 'requests' lo aggiungerà automaticamente con il boundary corretto.
        }

        # --- PIANO B: Forzatura MIME Type ---
        # Azure a volte rifiuta il file se non gli diciamo ESPLICITAMENTE che è un PDF.
        # Costruiamo una tupla: (NomeFileFinto, DatiFile, TipoMimeEsplicito)
        files_payload = {
            'document': ('source_document.pdf', file_content, 'application/pdf')
        }

        # 4. Esecuzione Chiamata
        response = requests.post(url, headers=headers, files=files_payload)
        
        # 5. Gestione Errori Azure
        if response.status_code != 200:
            error_msg = f"Errore Azure ({response.status_code}): {response.text}"
            print(error_msg) # Questo finisce nei log di Vercel
            return Response(error_msg, status=500)
            
        # 6. Restituzione PDF Tradotto
        return Response(
            response.content,
            mimetype="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=tradotto_{target_lang}.pdf",
                "Content-Type": "application/pdf"
            }
        )

    except Exception as e:
        return Response(f"Errore interno del server (Python): {str(e)}", status=500)

# Necessario per l'ambiente locale
if __name__ == '__main__':
    app.run()