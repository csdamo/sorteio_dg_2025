import os
import csv
import secrets
from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configurações a partir de variáveis de ambiente
app.secret_key = os.getenv('FLASK_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'uploads')
app.config['ALLOWED_EXTENSIONS'] = set(os.getenv('ALLOWED_EXTENSIONS', 'csv').split(','))

# Garante que as pastas de upload existam
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'evento'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'bolsa'), exist_ok=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def ler_participantes(arquivo_csv):
    participantes = []
    try:
        with open(arquivo_csv, mode='r', encoding='utf-8') as file:
            # Detecta o delimitador automaticamente
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
            reader = csv.DictReader(file, dialect=dialect)
            
            # Normaliza os nomes das colunas (remove espaços extras, etc.)
            fieldnames = [name.strip() for name in reader.fieldnames]
            reader.fieldnames = fieldnames
            
            for row in reader:
                participantes.append({
                    'timestamp': row.get('Carimbo de data/hora', ''),
                    'nome': row.get('Seu nome', ''),
                    'email': row.get('Seu e-mail', ''),
                    'telefone': row.get('Número de telefone', '')
                })
    except Exception as e:
        flash(f"Erro ao ler o arquivo: {str(e)}", 'error')
    return participantes

def sortear_participante(participantes, sorteados):
    disponiveis = [p for p in participantes if p['nome'] not in sorteados]
    if not disponiveis:
        return None
    return secrets.choice(disponiveis)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    tipo_sorteio = request.form.get('tipo_sorteio')
    session['tipo_sorteio'] = tipo_sorteio
    
    # Verifica se o arquivo foi enviado
    if 'arquivo_csv' not in request.files:
        flash('Nenhum arquivo enviado', 'error')
        return redirect(url_for('index'))
    
    file = request.files['arquivo_csv']
    
    # Verifica se o arquivo tem nome
    if file.filename == '':
        flash('Nenhum arquivo selecionado', 'error')
        return redirect(url_for('index'))
    
    # Verifica a extensão do arquivo
    if file and allowed_file(file.filename):

        # Define o caminho de salvamento
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], tipo_sorteio)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Remove arquivos antigos do mesmo tipo de sorteio
        for existing_file in os.listdir(upload_dir):
            os.remove(os.path.join(upload_dir, existing_file))
        
        # Salva o novo arquivo
        filename = f"participantes_{tipo_sorteio}.csv"
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        
        # Lê os participantes e armazena na sessão
        participantes = ler_participantes(filepath)
        if not participantes:
            flash('O arquivo está vazio ou no formato incorreto', 'error')
            return redirect(url_for('index'))
        
        session['participantes'] = participantes
        session['sorteados'] = []
        session['arquivo_sorteio'] = filepath

        return redirect(url_for('realizar_sorteio'))
    else:
        flash('Tipo de arquivo não permitido. Envie apenas arquivos CSV.', 'error')
        return redirect(url_for('index'))

@app.route('/sorteio')
def realizar_sorteio():
    if 'tipo_sorteio' not in session or 'participantes' not in session:
        flash('Por favor, faça upload do arquivo de participantes primeiro', 'error')
        return redirect(url_for('index'))
    
    tipo_sorteio = session['tipo_sorteio']
    todos_participantes = session['participantes']
    sorteados = session.get('sorteados', [])
    
    return render_template('sorteio.html', 
                         tipo_sorteio=tipo_sorteio,
                         sorteados=sorteados,
                         todos_participantes=todos_participantes)

@app.route('/sortear', methods=['POST'])
def sortear():
    if 'tipo_sorteio' not in session or 'participantes' not in session:
        return redirect(url_for('index'))
    
    participantes = session.get('participantes', [])
    sorteados = session.get('sorteados', [])
    
    sorteado = sortear_participante(participantes, sorteados)
    
    if sorteado:
        sorteados.append(sorteado['nome'])
        session['sorteados'] = sorteados
        session['ultimo_sorteado'] = sorteado
    else:
        flash('Todos os participantes já foram sorteados!', 'info')
    
    return redirect(url_for('realizar_sorteio'))

@app.route('/encerrar_sorteio', methods=['POST'])
def encerrar_sorteio():
    confirmacao = request.form.get('confirmacao')
    
    if confirmacao == 'sim':
        session.pop('tipo_sorteio', None)
        session.pop('participantes', None)
        session.pop('sorteados', None)
        session.pop('arquivo_sorteio', None)
        flash('Sorteio encerrado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/detalhes_sorteado/<nome>')
def detalhes_sorteado(nome):
    participantes = session.get('participantes', [])
    for p in participantes:
        if p['nome'] == nome:
            return render_template('resultado.html', participante=p)
    flash('Participante não encontrado', 'error')
    return redirect(url_for('realizar_sorteio'))

if __name__ == '__main__':
    # Verifica se a secret key foi configurada
    if not app.secret_key:
        raise ValueError("A FLASK_SECRET_KEY não está configurada no arquivo .env")
    
    app.run(debug=True)