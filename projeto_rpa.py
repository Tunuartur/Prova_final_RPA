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