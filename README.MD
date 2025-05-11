📝 Descrição

Este projeto é um sistema de sorteio desenvolvido em Flask que permite:

Upload de arquivos CSV com participantes

Realização de sorteios aleatórios

Visualização dos resultados

Gerenciamento de múltiplos sorteios


🛠️ Pré-requisitos

Antes de começar, verifique se você possui instalado em sua máquina:

Python 3.13 ou superior

pip (gerenciador de pacotes do Python)

Git (opcional, para clonar o repositório)


🚀 Instalação Local

Siga estes passos para configurar o projeto em sua máquina local:

1. Clone o repositório (ou baixe os arquivos)
bash
git clone https://github.com/csdamo/sorteio_dg_2025.git
cd sorteio-flask

2. Crie um ambiente virtual (recomendado)
bash
python -m venv venv
Ative o ambiente virtual:
Windows:

bash
venv\Scripts\activate

Linux/MacOS:

bash
source venv/bin/activate

3. Instale as dependências
bash
pip install -r requirements.txt

4. Configure o arquivo .env
Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

env
FLASK_SECRET_KEY=sua_chave_secreta_32_caracteres_aqui
UPLOAD_FOLDER=uploads
ALLOWED_EXTENSIONS=csv
Substitua sua_chave_secreta_32_caracteres_aqui por uma string segura (você pode gerar uma usando este comando Python: python -c "import secrets; print(secrets.token_hex(16))").

5. Estrutura de pastas
Crie as pastas necessárias:

bash
mkdir -p uploads/carro uploads/computador


🏃 Executando o Projeto

Execute o aplicativo com:

bash
python app.py
O servidor Flask será iniciado e você poderá acessar o sistema em:

http://localhost:5000


📊 Como Usar

Página Inicial:

Selecione o tipo de sorteio (Carro ou Computador)

Faça upload do arquivo CSV com os participantes

Formato do CSV:

O arquivo deve conter colunas com os cabeçalhos:

"Carimbo de data/hora"

"Seu nome"

"Seu e-mail"

"Número de telefone"

Realizando Sorteios:

Após o upload, clique em "Sortear Próximo" para realizar os sorteios

Os nomes sorteados aparecerão na tela

Clique em um nome para ver detalhes completos

Encerrando Sorteios:

Use o botão "Encerrar Sorteio" para finalizar

Confirme a ação quando solicitado
