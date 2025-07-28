# 🏎️⚙️ Assetto Corsa Stints (ACS) Em desenvolvimento

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/Otavio72/Impressa/blob/main/LICENSE)

**ACS** durante a minha participação num campeonato de assetto corsa na WSS (Word Sim Series) nos treinos identifiquei a necessidade de uma medicao e analise dos stints(sequencias de voltas) e a partir disso veio a ideia do ACS

---

## 🛠️ Sobre o projeto

é uma aplicação local que extrai tempos de volta do jogo assetto corsa envia para um servidor onde os dados sao armazenados num SQL e recuperados pelo programa principal que cria um grafico com 2 stints e envia para a API do GEMINI onde o mesmo esta interpretando um eng de corridas que analisa e da feedback dos stints via chatbot

### Funcionalidades principais:

- 🧾 Extração de dados via **Shared Memory** baseado num mod template feito por **Hunter Vaners** https://github.com/huntervaners/Template_Assetto_Corsa_App
- 🛒 Visualização de dados por grafico **matplotlib**
- 🔐 Engenheiro Virtual com **GEMINI**
- 📚 Armazenamento de dados com **MySql**
- 🌙 Interface **CustomTkinter**

---

## 💻 Layout da aplicação

### Página inicial e orçamento
![Página Inicial](https://github.com/Otavio72/assets/blob/main/impressa1.png)
![Orçamento](https://github.com/Otavio72/assets/blob/main/impressa4.png)

### Sobre o projeto e modo escuro
![Sobre o projeto](https://github.com/Otavio72/assets/blob/main/impressa5.png)
![Modo escuro](https://github.com/Otavio72/assets/blob/main/impressaescuro.png)

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
