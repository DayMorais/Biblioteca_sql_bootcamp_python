'''
DB autor
Documentação de apoio: https://www.sqlitetutorial.net/
'''

from sqlite3 import Connection


def drop_table_autores(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS autores")


def criar_tabela_autores(db_conection: Connection)-> None:
    '''
    Cria a tabela autores
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS autores(
                    id integer primary key autoincrement,
                    nome text UNIQUE NOT NULL)''')

    db_conection.commit()


def insert_autor(db_conection: Connection, nome: str) -> None:
    '''
    Inseri autor na tabela.
    '''
    db_conection.cursor().execute("INSERT INTO autores(nome) VALUES(?)", (nome,))
    db_conection.commit()


def consultar_por_autor(db_conection: Connection, nome_autor: str) -> list:
    '''
    Consulta livros de um autor específico.
    '''
    cursor = db_conection.cursor()
    cursor.execute('SELECT id FROM autores WHERE nome = ?', (nome_autor,))
    autor_id = cursor.fetchone()
    
    if(autor_id):
        autor_id = autor_id[0]:
        cursor.execute('SELECT titulo FROM livros WHERE autor_id = ?', (autor_id,))
        autor_id = cursor.fetchall()
        return [livro[0] for livro in livros]
    else:
        return[]


