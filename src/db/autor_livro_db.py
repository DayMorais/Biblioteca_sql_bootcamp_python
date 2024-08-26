'''
DB autores_livros
Documentação de apoio: https://www.sqlitetutorial.net/sqlite-foreign-key/
'''
from sqlite3 import Connection


def drop_table_autores_livros(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS autores_livros")


def criar_tabela_autores_livros(db_conection: Connection)-> None:
    '''
    Cria a tabela autores_livros
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS autores_livros(
                    autor_id integer NOT NULL,
                    livro_id interger NOT NULL,
                    PRIMARY KEY (livro_id, autor_id),
                    FOREIGN KEY(livro_id) REFERENCES livros(id)
                        ON DELETE CASCADE,
                    FOREIGN KEY(autor_id) REFERENCES autores(id)
                        ON DELETE RESTRICT)''')

    db_conection.commit()


def insert_autores_livros(db_conection: Connection, autor_id: int, livro_id: int) -> None:
    '''
    Inseri autor_id e livro_id na tabela.
    '''
    dados = (autor_id, livro_id)
    db_conection.cursor().execute('INSERT INTO autores_livros(autor_id, livro_id) VALUES(?, ?)', dados)
    db_conection.commit()


def remover_autor(db_conection: Connection, nome_autor: str) -> None:
    '''
    Remove um autor específico e suas referências.
    '''
    cursor = db_conection.cursor()
    cursor.execute('DELETE FROM autores_livros WHERE autor_id = (SELECT id FROM autores WHERE nome = ?)', (nome_autor,))
    cursor.execute('DELETE FROM autores WHERE nome = ?', (nome_autor,))
    
    db_conection.commit()
