from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

# CONFIGURAZIONE (Questi valori li prenderemo dalle variabili d'ambiente di Vercel)
AZURE_KEY = os.environ.get('AZURE_KEY')
AZURE_ENDPOINT = os.environ.get('AZURE_ENDPOINT') # Esempio: https://api.cognitive.microsofttranslator.com/
APP_PASSWORD = os.environ.get('APP_PASSWORD')

@app.route('/api/traduci', methods=['POST'])
def handler():
    # 1. Controllo Sicurezza (Password)
    user_pass = request.headers.get('x-app-password')
    if user_pass != APP_PASSWORD:
        return Response("Password errata/Non autorizzato", status=401)

    # 2. Controllo File
    if 'file' not in request.files:
        return Response("Nessun file caricato", status=400)
    
    file = request.files['file']
    target_lang = request.form.get('target_lang', 'it')

    # 3. Chiamata ad Azure (Synchronous Document Translation)
    # Documentazione: POST /translator/document:translate
    url = f"{AZURE_ENDPOINT}/translator/document:translate?sourceLanguage=en&targetLanguage={target_lang}&api-version=2024-05-01"
    
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
    }

    # Creiamo il payload multipart come vuole Azure
    files_payload = {
        'document': (file.filename, file.stream, 'application/pdf')
    }

    try:
        # Invio ad Azure
        response = requests.post(url, headers=headers, files=files_payload)
        
        # Se Azure restituisce errore
        if response.status_code != 200:
            return Response(f"Errore Azure: {response.text}", status=500)

        # 4. Restituisci il PDF tradotto al browser
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