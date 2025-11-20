import os
from flask import Flask, request, render_template, redirect, url_for
import werkzeug.utils

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limite 16MB

# Cria pasta uploads se não existir
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    # Renderiza template com mensagem opcional
    message = request.args.get('message')
    return render_template('index.html', message=message)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index', message="Nenhum arquivo selecionado."))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index', message="Nenhum arquivo selecionado."))
    if file:
        filename = werkzeug.utils.secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index', message="Arquivo enviado com sucesso!"))
    return redirect(url_for('index'))

@app.route('/upload', methods=['GET'])
def upload_get():
    # Retorna erro para acesso errado via GET
    return "Método GET não permitido na rota /upload.", 405


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
