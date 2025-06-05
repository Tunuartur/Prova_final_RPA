import requests
import sqlite3

url = "https://rickandmortyapi.com/api/character"
response = requests.get(url)
data = response.json()
personagens = data['results']

conn = sqlite3.connect('projeto_rpa.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS personagens (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        status TEXT,
        especie TEXT,
        genero TEXT,
        localizacao TEXT
    )
''')

for p in personagens:
    cursor.execute('''
        INSERT OR REPLACE INTO personagens (id, nome, status, especie, genero, localizacao)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        p['id'],
        p['name'],
        p['status'],
        p['species'],
        p['gender'],
        p['location']['name']
    ))

conn.commit()
conn.close()

print("Dados inseridos no banco de dados com sucesso!")

import re

conn = sqlite3.connect('projeto_rpa.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dados_processados (
        id INTEGER PRIMARY KEY,
        nome TEXT,
        genero TEXT,
        localizacao TEXT
    )
''')

cursor.execute("SELECT id, nome, genero, localizacao FROM personagens")
todos = cursor.fetchall()

padrao_genero = re.compile(r'^Male$', re.IGNORECASE)
padrao_local = re.compile(r'earth', re.IGNORECASE)

for id_, nome, genero, local in todos:
    if padrao_genero.search(genero) and padrao_local.search(local):
        cursor.execute('''
            INSERT OR REPLACE INTO dados_processados (id, nome, genero, localizacao)
            VALUES (?, ?, ?, ?)
        ''', (id_, nome, genero, local))

conn.commit()
conn.close()

print("Dados processados e inseridos na tabela dados_processados com sucesso!")

import sqlite3
import smtplib
from email.message import EmailMessage
import getpass

conn = sqlite3.connect('projeto_rpa.db')
cursor = conn.cursor()
cursor.execute("SELECT nome, genero, localizacao FROM dados_processados")
dados = cursor.fetchall()
conn.close()

resumo = "Resumo dos personagens processados:\n\n"
for nome, genero, local in dados:
    resumo += f"Nome: {nome}\nGênero: {genero}\nLocalização: {local}\n\n"

print("=== Configuração do e-mail ===")
EMAIL_ORIGEM = input("Seu e-mail Gmail: ")
EMAIL_SENHA = input("Senha de app do Gmail (senha gerada pelo email!): ")
EMAIL_DESTINO = input("E-mail de destino: ")

msg = EmailMessage()
msg['Subject'] = 'Relatório Final RPA - Personagens de Rick and Morty'
msg['From'] = EMAIL_ORIGEM
msg['To'] = EMAIL_DESTINO
msg.set_content(resumo)

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ORIGEM, EMAIL_SENHA)
        smtp.send_message(msg)
    print("✅ E-mail enviado com sucesso!")
except Exception as e:
    print("❌ Falha ao enviar e-mail:", e)
