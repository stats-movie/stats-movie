from conexao_db import abrir_conexao, abrir_conexao_database, fechar_conexao
from hasher import senha_hash, verifica_senha



# Cria o banco de dados stats_movie e suas tabelas
def criar_database():

    # initial_con = abrir_conexao_database("localhost", "estudante1", "1234")
    initial_con = abrir_conexao_database("localhost", "root", "Motta313.")

    sql = """
    CREATE DATABASE if not exists stats_movie;
    USE stats_movie;
    CREATE TABLE if not exists usuarios(
    id_usuario INTEGER PRIMARY KEY NOT NULL auto_increment,
    data_nascimento DATE,
    numero_celular CHAR(11),
    nome VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(1000) NOT NULL,
    nome_usuario VARCHAR(50) NOT NULL,
    foto_perfil VARCHAR(255),
    pontos INTEGER,
    UNIQUE (nome_usuario),
    UNIQUE(email));
    """
    cursor = initial_con.cursor(dictionary=True)
    cursor.execute(sql)

    cursor.close()

# Lista um campo de um usuário
# dependendo como ele logou utiliza o nome de usuário ou o email

def usuario_listar(usuario, campo):
    # con = abrir_conexao("localhost", "estudante1", "1234", "stats_movie")
    con = abrir_conexao("localhost", "root", "Motta313.", "stats_movie")
    tipo = "nome_usuario"
    for char in list(usuario):
        if char == '@':
            tipo = "email"
    sql = f"SELECT {campo} FROM usuarios WHERE {tipo} = '{usuario}'" 
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)
    for (registro) in cursor:
        resultado = registro[f"{campo}"]
    cursor.close()
    return resultado

# checa se o usuário está no banco de dados e se estiver se a senha é válida
def usuario_checar(usuario, senha):
    # con = abrir_conexao("localhost", "estudante1", "1234", "stats_movie")
    con = abrir_conexao("localhost", "root", "Motta313.", "stats_movie")
    tipo = "nome_usuario"
    for char in list(usuario):
        if char == '@':
            tipo = "email"
    sql = f"SELECT {tipo} FROM usuarios WHERE {tipo}='{usuario}'"
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = 0
    for (registro) in cursor:
        if str(registro) != "":
            resultado = registro[f'{tipo}']

    if resultado == 0:
        return 1
    
    sql = f"SELECT senha FROM usuarios WHERE {tipo}='{usuario}'"
    cursor.execute(sql)
    for (i) in cursor:
        hash = i['senha']
        a = verifica_senha(senha, hash)
        if(a == False):
            return 2
        

    return 0

# inseri os dados do usuário no banco de dados (dados base da página de cadastro)
def usuario_inserir(nome_usuario, email, senha, nome):
    # con = abrir_conexao("localhost", "estudante1", "1234", "stats_movie")
    con = abrir_conexao("localhost", "root", "Motta313.", "stats_movie")
    cursor = con.cursor(dictionary=True)
    sql = f"INSERT INTO usuarios (nome_usuario, email, senha, nome) VALUES ('{nome_usuario}', '{email}', '{senha}', '{nome}')"
    cursor.execute(sql)
    con.commit() 
    cursor.close()

def usuario_atualizar(nome_usuario_antigo, nome_usuario, email, senha, nome, data_nascimento = "", numero_celular = "", foto_perfil = ""):
    # con = abrir_conexao("localhost", "estudante1", "1234", "stats_movie")
    con = abrir_conexao("localhost", "root", "Motta313.", "stats_movie")
    cursor = con.cursor(dictionary=True)
    print(f"'{nome_usuario_antigo}'")
    data = ""
    numero = ""
    foto = ""
    sen = ""
    if data_nascimento != "":
        data = ", data_nascimento = "
        data_nascimento = f"'{data_nascimento}'"
    if numero_celular != "":
        numero = ", numero_celular = "
    if foto_perfil != "":
        foto = ", foto_perfil = "
        foto_perfil = f"'{foto_perfil}'"
    if senha != "":
        sen = ", senha = "
        senha = f"'{senha}'"
    sql = f"UPDATE usuarios SET nome_usuario = '{nome_usuario}', email = '{email}', nome = '{nome}'{sen}{senha}{data}{data_nascimento}{numero}{numero_celular}{foto}{foto_perfil} WHERE nome_usuario = '{nome_usuario_antigo}';"
    cursor.execute(sql)
    con.commit() 
    cursor.close()