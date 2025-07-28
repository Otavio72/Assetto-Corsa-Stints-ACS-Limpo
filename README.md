# 🏎️⚙️ Assetto Corsa Stints (ACS) Em desenvolvimento

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Otavio72/Assetto-Corsa-Stints-ACS-/blob/main/LICENSE)

**ACS** surgiu durante minha participação em um campeonato da **World Sim Series (WSS)**. Nos treinos, percebi a necessidade de uma análise mais detalhada dos stints (sequências de voltas), o que inspirou a criação deste projeto.

---

## 🛠️ Sobre o projeto

O **ACS** é uma aplicação local que extrai dados de telemetria do jogo Assetto Corsa, envia os tempos de volta para um servidor com banco de dados **MySQL**, e os recupera para gerar gráficos comparativos entre dois stints. Esses dados são enviados à API do **GEMINI**, onde um "engenheiro virtual" interpreta os resultados e fornece feedback técnico via chatbot.


### Funcionalidades principais:

- 🧾 Extração de dados via **Shared Memory**, com base no mod template de [Hunter Vaners](https://github.com/huntervaners/Template_Assetto_Corsa_App)
- 📈 Geração de gráficos comparativos com **Matplotlib**
- 🤖 Feedback técnico com **GEMINI API**
- 💾 Armazenamento em banco de dados **MySQL**
- 🌙 Interface gráfica com **CustomTkinter**
- 🔌 Comunicação entre cliente e servidor via Sockets com select para conexões simultâneas

---

## 💻 Layout da aplicação

### Página inicial
![Página Inicial](https://github.com/Otavio72/assets/blob/main/acs1.png)

### Página de Status
![Página de Status](https://github.com/Otavio72/assets/blob/main/acs2.png)

### Menu de Stints
![Menu de Stints](https://github.com/Otavio72/assets/blob/main/acs3.png)

### Pagina de analise
![Pagina de analise](https://github.com/Otavio72/assets/blob/main/acs4.png)

### Datalogger no jogo
![Datalogger no jogo](https://github.com/Otavio72/assets/blob/main/acs5.png)

---

## 🗂️ GIFs

![Modelo Conceitual](https://github.com/Otavio72/assets/blob/main/modelo_impressa.png)

---

## 🚀 Tecnologias utilizadas

### 🔙 Back end
- Python

### 🔙 Banco de dados
- MySQL

### 🎨 Interface
- CustomTkinter

---

## ⚙️ Como executar o projeto

### ATENÇÃO
Para rodar o ACSv9 e necessario ter o jogo assetto corsa instalado para que os dados sejam extraidos caso
contrario o programa nao vai funcionar
por conta desse problema desenvolvi o ACSvDEMO baseado numa versao anterior do acs que utilizava arquivos .csv
dentro da pasta DEMO esta residido o ACSvDEMO com arquivos .csv para serem selecionados e analisados
adptei o menu de selecao de stints para funcionar de forma similar a versao completa


### ✅ Pré-requisitos

- Python 3.11+
- Ambiente virtual configurado

### 📦 Instalação

```bash
# clonar repositório
git clone https://github.com/Otavio72/Impressa

Ative o ambiente virtual:
  python -m venv .venv

No Windows (PowerShell):
  ```powershell
  .venv\Scripts\Activate.ps1

No Linux/macOS:
  source .venv/bin/activate

Instale as dependências:
  pip install -r requirements.txt

Rode as migrações do banco de dados
  python manage.py migrate

python manage.py runserver

Acesse o projeto no navegador:
http://127.0.0.1:8000/
```
👤 Como acessar o sistema
Para acessar o Impressa, faça seu cadastro:
1. Acesse: http://127.0.0.1:8000/usuarios/register/
2. Preencha o formulário de cadastro
3. Após o registro, você será redirecionado para a página inicial

# Autor
Otávio Ribeiro
www.linkedin.com/in/otávio-ribeiro-57a359197
