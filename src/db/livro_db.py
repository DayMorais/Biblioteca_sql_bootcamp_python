'''
Módulo livro DB
Documentação de apoio: https://www.sqlitetutorial.net/
'''

from sqlite3 import Connection


def drop_table_livros(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS livros")


def criar_tabela_livros(db_conection: Connection)-> None:
    '''
    Cria a tabela livros
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS livros(
                    id integer primary key autoincrement,
                    titulo text NOT NULL,
                    renovacoes_permitidas integer NOT NULL,                  
                    editora_id integer NOT NULL,
                    FOREIGN KEY(editora_id) REFERENCES editoras(id)
                   )''')


    db_conection.commit()


def insert_livro(
    db_conection: Connection,
    titulo: str,
    renovacoes_permitidas: int,
    editora_id: int
) -> None:
    '''
    Inseri livro na tabela.
    '''
    dados =  (
        titulo,
        renovacoes_permitidas,
        editora_id
    )
    db_conection.cursor().execute('INSERT INTO livros(titulo, renovacoes_permitidas, editora_id) VALUES(?, ?, ?)', dados) # pylint: disable=line-too-long
    db_conection.commit()
