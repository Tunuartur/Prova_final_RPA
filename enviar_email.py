import sqlite3
import smtplib
from email.message import EmailMessage

conn = sqlite3.connect('projeto_rpa.db')
cursor = conn.cursor()
cursor.execute("SELECT nome, genero, localizacao FROM dados_processados")
dados = cursor.fetchall()
conn.close()

resumo = "Resumo dos personagens processados:\n\n"
for nome, genero, local in dados:
    resumo += f"Nome: {nome}\nGênero: {genero}\nLocalização: {local}\n\n"

EMAIL_ORIGEM = 'SEU_EMAIL_@gmail.com'
EMAIL_SENHA = 'SENHA_DE_APLICATIVO_AQUI'
EMAIL_DESTINO = 'EMAIL_DESEJADO_@gmail.com'

msg = EmailMessage()
msg['Subject'] = 'Relatório Final RPA - Personagens de Rick and Morty'
msg['From'] = EMAIL_ORIGEM
msg['To'] = EMAIL_DESTINO
msg.set_content(resumo)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ORIGEM, EMAIL_SENHA)
    smtp.send_message(msg)

print("E-mail enviado com sucesso!")