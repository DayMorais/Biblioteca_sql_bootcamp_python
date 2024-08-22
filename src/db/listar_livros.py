from sqlite3 import Connection
from src.db.conexao_db import get_conexao_db

def listar_livros (conexao: Connection, nome_tabela: str):
    cursor = conexao.cursor()
    lista = cursor.execute(f'SELECT * FROM {nome_tabela}')
    
    for livro in lista:
        print (livro)
