<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Traduttore Aziendale</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 8px 20px rgba(0,0,0,0.1); width: 100%; max-width: 420px; text-align: center; }
        h2 { color: #0078D4; margin-bottom: 25px; }
        label { display: block; text-align: left; font-weight: 600; margin-top: 15px; margin-bottom: 5px; color: #333; }
        input, select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 14px; }
        button { background: #0078D4; color: white; border: none; padding: 14px; width: 100%; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 25px; transition: background 0.3s; }
        button:hover { background: #005a9e; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        #status { margin-top: 20px; font-size: 14px; line-height: 1.5; }
        .error { color: #d93025; font-weight: bold; }
        .success { color: #188038; font-weight: bold; }
        .warning { color: #e37400; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Traduttore Aziendale</h2>
        
        <label>1. Password Aziendale</label>
        <input type="password" id="appPass" placeholder="Inserisci la password..." required>

        <label>2. Scegli il PDF (Max 4.5MB)</label>
        <input type="file" id="pdfFile" accept=".pdf" required>

        <label>3. Lingua di Destinazione</label>
        <select id="targetLang">
            <option value="it">Italiano 🇮🇹</option>
            <option value="en">Inglese 🇬🇧</option>
            <option value="es">Spagnolo 🇪🇸</option>
            <option value="de">Tedesco 🇩🇪</option>
            <option value="fr">Francese 🇫🇷</option>
            <option value="pt">Portoghese 🇵🇹</option>
            <option value="nl">Olandese 🇳🇱</option>
        </select>

        <button onclick="traduci()" id="btn">Traduci Documento</button>
        <div id="status"></div>
    </div>

    <script>
        async function traduci() {
            const pass = document.getElementById('appPass').value;
            const fileInput = document.getElementById('pdfFile');
            const file = fileInput.files[0];
            const lang = document.getElementById('targetLang').value;
            const status = document.getElementById('status');
            const btn = document.getElementById('btn');

            // Reset messaggi
            status.innerHTML = "";

            // 1. Validazione Base
            if (!pass || !file) { 
                status.innerHTML = "<span class='error'>⚠️ Devi inserire password e file!</span>"; 
                return; 
            }

            // 2. Validazione Peso File (Vercel Free Limit: 4.5MB)
            const fileSizeMB = file.size / 1024 / 1024;
            if (fileSizeMB > 4.4) {
                status.innerHTML = `
                    <span class='error'>❌ File troppo grande (${fileSizeMB.toFixed(2)} MB).</span><br>
                    <span class='warning'>Il limite è 4.5 MB.</span><br>
                    <a href="https://www.ilovepdf.com/it/comprimere_pdf" target="_blank" style="color:#0078D4">Clicca qui per comprimerlo gratis</a>
                `;
                return;
            }

            // Preparazione invio
            btn.disabled = true;
            btn.innerText = "Traduzione in corso...";
            status.innerHTML = "⏳ Caricamento e traduzione (può richiedere fino a 30 sec)...";

            const formData = new FormData();
            formData.append('file', file);
            formData.append('target_lang', lang);

            try {
                const response = await fetch('/api/traduci', {
                    method: 'POST',
                    headers: { 'x-app-password': pass },
                    body: formData
                });

                if (!response.ok) {
                    const errText = await response.text();
                    throw new Error(errText || "Errore sconosciuto del server");
                }

                // Download del file
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Tradotto_${lang}_${file.name}`;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                
                status.innerHTML = "<span class='success'>✅ Fatto! Il download dovrebbe partire.</span>";
                fileInput.value = ""; // Reset input file
            } catch (e) {
                console.error(e);
                status.innerHTML = "<span class='error'>❌ Errore: " + e.message + "</span>";
            } finally {
                btn.disabled = false;
                btn.innerText = "Traduci Documento";
            }
        }
    </script>
</body>
</html>