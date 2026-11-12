import sqlite3
from datetime import datetime

def criar_tabela():
    with sqlite3.connect('ranking.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ranking (
                id INTEGER PRIMARY KEY,
                pontuacao_maior INTEGER NOT NULL DEFAULT 0
            )
    ''')
        cursor.execute('''
            INSERT OR IGNORE INTO ranking (id, pontuacao_maior)
            VALUES (1, 0)             
    ''')
        
def pontos():
    with sqlite3.connect('ranking.db') as conexao:
        cursor = conexao.cursor()
        
        cursor.execute('''
        SELECT pontuacao_maior FROM ranking WHERE id = 1
''')
        
    resultado = cursor.fetchone()
    return resultado[0]

def pontos_recorde(score):
    recorde = pontos()
    
    if score > recorde:
        
        with sqlite3.connect('ranking.db') as conexao:
            cursor = conexao.cursor()
            
            cursor.execute('''
                UPDATE ranking SET pontuacao_maior = ? WHERE id = 1
        ''', (score,))
            
        return score
    
    return recorde