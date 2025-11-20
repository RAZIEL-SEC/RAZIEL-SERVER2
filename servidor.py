#atualizando o servidor.py
#clonei o repo
from flask import Flask, request, render_template, redirect, url_for
import os
import werkzeug.utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Pasta para uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite de 16MB por arquivo

# Certifique-se de que a pasta de uploads existe
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')  # Mantém o visual original

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        filename = werkzeug.utils.secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Arquivo enviado com sucesso!'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 6969))  # Porta dinâmica para hospedagem
    app.run(host='0.0.0.0', port=port, debug=False)  # Roda em 0.0.0.0 para internet
