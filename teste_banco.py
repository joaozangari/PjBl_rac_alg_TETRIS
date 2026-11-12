import sqlite3

conexao = sqlite3.connect('ranking.db')
cursor = conexao.cursor()

cursor.execute('SELECT * FROM ranking')

resultado = cursor.fetchall()

print("Dados armazenados no banco:")

for linha in resultado:
    print(linha)

conexao.close()