'''
Módulo exemplar DB
Documentação de apoio: https://www.sqlitetutorial.net/
'''

from sqlite3 import Connection
from conexao_db import get_conexao_db


def drop_table_exemplares(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS exemplares")


def criar_tabela_exemplares(db_conection: Connection) -> None:
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
    dados = (
        disponivel,
        livro_id
    )
    db_conection.cursor().execute('INSERT INTO exemplares(disponivel, livro_id) VALUES(?, ?)',
                                  dados)  # pylint: disable=line-too-long
    db_conection.commit()


def verificar_copias_disponiveis(
    db_conection: Connection,
    livro_id: int
) -> int:
    '''
    Verifica o número de cópias disponíveis de um determinado livro.
    Retorna o número de exemplares disponíveis para o livro especificado.
    '''
    cursor = db_conection.cursor()
    cursor.execute(
        'SELECT COUNT(*) FROM exemplares WHERE livro_id = ? AND disponivel = 1', (livro_id,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else 0


# Criando a tabela exemplares
criar_tabela_exemplares(db_connection)

# Inserindo um exemplar de exemplo
insert_exemplar(db_connection, livro_id=1, disponivel=1)

# Verificando o número de cópias disponíveis do livro com ID 1
numero_copias = verificar_copias_disponiveis(db_connection, livro_id=1)
print(f'Número de cópias disponíveis: {numero_copias}')
