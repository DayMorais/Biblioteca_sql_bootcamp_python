'''
DB emprestimo
Documentação de apoio: https://www.sqlitetutorial.net/
'''
from typing import Any
from datetime import datetime
from sqlite3 import Connection

def drop_table_emprestimos(db_conection: Connection) -> None:
    '''
    Apaga a tabela se ela já exixtir.
    '''
    db_conection.cursor().execute("DROP TABLE IF EXISTS emprestimos")


def criar_tabela_emprestimos(db_conection: Connection)-> None:
    '''
    Cria a tabela emprestimos
    '''
    db_conection.cursor().execute(''' CREATE TABLE IF NOT EXISTS emprestimos(
                    id integer primary key autoincrement,
                    usuario_id integer NOT NULL,
                    livro_id integer NOT NULL,
                    exemplar_id integer NOT NULL,
                    numero_de_renovacoes integer NOT NULL,
                    estado text NOT NULL,
                    data_emprestimo text NOT NULL,
                    data_para_devolucao text NOT NULL,
                    data_devolucao text,
                    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                    FOREIGN KEY(livro_id) REFERENCES livros(id),
                    FOREIGN KEY(exemplar_id) REFERENCES exemplares(id))''')

    db_conection.commit()


def insert_emprestimo(
        db_conection: Connection,
        usuario_id: int,
        livro_id: int,
        exemplar_id: int,
        estado: str,
        data_emprestimo: datetime,
        data_para_devolucao: datetime,
        data_devolucao: datetime | None,
        numero_de_renovacoes: int = 0,
) -> None:
    '''
    Inseri emprestimo na tabela.
    '''
    dados =  (
        usuario_id,
        livro_id,
        exemplar_id,
        numero_de_renovacoes,
        estado,
        data_emprestimo,
        data_para_devolucao,
        data_devolucao
    )

    db_conection.cursor().execute('INSERT INTO emprestimos(usuario_id, livro_id, exemplar_id, numero_de_renovacoes, estado, data_emprestimo, data_para_devolucao, data_devolucao) VALUES(?, ?, ?, ?, ?, ?, ?, ?)', dados) # pylint: disable=line-too-long
    db_conection.commit()


##########################################################################
    # INTERFACE DE RESPOSTA PARA COUNT #
##########################################################################

def tuple_to_dict(data: tuple) -> dict[str, Any]:
    '''
    Transforma um elemento (tuple) do banco de dados em uma estrutura de dicionário.
    Retorna o dicionário com dados.
    '''
    if not data:
        return {}

    (
        identificacao,
        usuario_id,
        livro_id,
        exemplar_id,
        numero_de_renovacoes,
        estado,
        data_emprestimo,
        data_para_devolucao,
        data_devolucao,
        usuario_nome,
        livro_titulo,
        livro_numero_renovacoes,
        editora_nome
        

     ) =  data


    return {
        'id': identificacao,
        'usuario_id': usuario_id,
        'livro_id': livro_id,
        'exemplar_id': exemplar_id,
        'numero_de_renovacoes': numero_de_renovacoes,
        'estado': estado,
        'data_emprestimo': data_emprestimo,
        'data_para_devolucao': data_para_devolucao,
        'data_devolucao': data_devolucao if data_devolucao else None,
        'usuario_nome': usuario_nome,
        'livro_titulo': livro_titulo,
        'livro_numero_renovacoes': livro_numero_renovacoes,
        'editora_nome': editora_nome
    }

def get_emprestimos_atrasados(db_conection: Connection, ) -> list[dict[str, int]]:
    '''
    Obter todos os emprestimos em atraso
    '''
    cursor = db_conection.cursor()
    cursor.execute("""SELECT e.id, e.usuario_id, e.livro_id, e.exemplar_id, e.numero_de_renovacoes, e.estado,
                        e.data_emprestimo, e.data_para_devolucao, e.data_devolucao,
                        u.nome AS usuario_nome, l.titulo AS livro_titulo, l.renovacoes_permitidas AS livro_numero_renovacoes,
                        ed.nome AS editora_nome
                        FROM emprestimos AS e
                        INNER JOIN usuarios AS u ON (u.id = e.usuario_id)
                        INNER JOIN livros  AS l ON (l.id = e.livro_id)
                        INNER JOIN editoras AS ed ON (ed.id = l.editora_id)
                        WHERE  e.estado = 'EMPRESTADO' AND e.data_para_devolucao  < date('now','localtime')
                    """)


    emprestimos_db = cursor.fetchall()
    result: list[dict[str, int]] = []
    for data in emprestimos_db:
        emprestimo = tuple_to_dict(data)
        result.append(emprestimo)
    return result
