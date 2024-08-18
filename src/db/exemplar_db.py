'''
Módulo exemplar DB
Documentação de apoio: https://www.sqlitetutorial.net/
'''

from sqlite3 import Connection


def drop_table_exemplares(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS exemplares")


def criar_tabela_exemplares(db_conection: Connection)-> None:
    '''
    Cria a tabela exemplares
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS exemplares(
                    id integer primary key autoincrement,
                    disponivel integer NOT NULL,                  
                    livro_id integer NOT NULL,
                    FOREIGN KEY(livro_id) REFERENCES livros(id)
                        ON DELETE CASCADE)''')

    db_conection.commit()


def insert_exemplar(
    db_conection: Connection,
    livro_id: int,
    disponivel: int = 1,
) -> None:
    '''
    Inseri exemplar na tabela.
    '''
    dados =  (
        disponivel,
        livro_id
    )
    db_conection.cursor().execute('INSERT INTO exemplares(disponivel, livro_id) VALUES(?, ?)', dados) # pylint: disable=line-too-long
    db_conection.commit()
