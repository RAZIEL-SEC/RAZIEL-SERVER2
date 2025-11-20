from flask import Flask, request, render_template, redirect, url_for
import firebase_admin
from firebase_admin import credentials, storage
import os

app = Flask(__name__)

# Inicialize o Firebase com suas credenciais
# Substitua 'path/to/firebase-key.json' pelo caminho do arquivo baixado (ex.: 'firebase-key.json')
# No Render, faça upload do arquivo JSON e use o caminho relativo, ou use variáveis de ambiente para a chave.
cred = credentials.Certificate('firebase-key.json')  # Ou use uma variável de ambiente para segurança
firebase_admin.initialize_app(cred, {
    'storageBucket': 'seu-project-id.appspot.com'  # Substitua pelo seu Project ID + .appspot.com
})

bucket = storage.bucket()

# Função para listar arquivos no Firebase Storage
def list_firebase_files():
    try:
        blobs = bucket.list_blobs()
        return [blob.name for blob in blobs]
    except Exception as e:
        print(f"Erro ao listar arquivos: {e}")
        return []

# Função para fazer upload para Firebase
def upload_to_firebase(file, filename):
    try:
        blob = bucket.blob(filename)
        blob.upload_from_file(file)
        return True
    except Exception as e:
        print(f"Erro ao fazer upload: {e}")
        return False

@app.route('/')
def index():
    files = list_firebase_files()
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Erro: Nenhuma parte de arquivo encontrada.'
    
    file = request.files['file']
    if file.filename == '':
        return 'Erro: Nenhum arquivo selecionado.'
    
    # Validação básica (opcional)
    if not file.filename.lower().endswith(('.txt', '.pdf', '.jpg', '.png')):
        return 'Erro: Tipo de arquivo não permitido.'
    
    filename = file.filename  # Firebase lida com segurança automaticamente
    
    if upload_to_firebase(file, filename):
        return redirect(url_for('index'))
    else:
        return 'Erro: Falha no upload.'

@app.route('/download/<filename>')
def download(filename):
    try:
        blob = bucket.blob(filename)
        url = blob.generate_signed_url(expiration=3600)  # URL válida por 1 hora
        return redirect(url)
    except Exception as e:
        return f'Erro ao gerar link de download: {e}'

if __name__ == '__main__':
    app.run(debug=True)
