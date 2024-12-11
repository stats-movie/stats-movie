from conexao_db import abrir_conexao, abrir_conexao_database, fechar_conexao
con = abrir_conexao("localhost", "estudante1", "123", "stats_movie")
def criar_database():

    initial_con = abrir_conexao_database("localhost", "estudante1", "123")


    sql = """
    CREATE DATABASE if not exists stats_movie;
    USE stats_movie;
    CREATE TABLE if not exists usuarios(
    id_usuario INTEGER PRIMARY KEY NOT NULL auto_increment,
    data_nascimento DATE,
    numero_celular CHAR(11),
    nome VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(50) NOT NULL,
    nome_usuario VARCHAR(50) NOT NULL,
    foto_perfil VARCHAR(255),
    pontos INTEGER,
    UNIQUE (nome_usuario),
    UNIQUE(email));

    """
    # Criando o cursor com a opção de retorno como dicionário   
    cursor = initial_con.cursor(dictionary=True)
    cursor.execute(sql)

    cursor.close()


def usuario_listar(user, tipo, campo):
    sql = f"SELECT {campo} FROM usuarios WHERE {tipo} = '{user}'"
    # Criando o cursor com a opção de retorno como dicionário   
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)

    for (registro) in cursor:
        print(registro)
        resultado = registro[f"{campo}"]


    cursor.close()
    return resultado


def usuario_checar(user, tipo, senha):
    sql = f"SELECT {tipo} FROM usuarios WHERE {tipo}='{user}' and senha = '{senha}'"
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = 0
    for (registro) in cursor:
        if str(registro) != "":
            resultado = registro[f'{tipo}']

    return resultado

def usuario_inserir(nome_usuario, email, senha, nome):
    cursor = con.cursor(dictionary=True)
    sql = f"INSERT INTO usuarios (nome_usuario, email, senha, nome) VALUES ('{nome_usuario}', '{email}', '{senha}', '{nome}')"
    cursor.execute(sql)
    con.commit() 
    cursor.close()