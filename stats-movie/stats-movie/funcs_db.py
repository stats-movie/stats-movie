from conexao_db import abrir_conexao, fechar_conexao

def usuarios_listar():
    con = abrir_conexao("localhost", "estudante1", "123", "stats_movie")
    sql = "SELECT * FROM usuarios"
    # Criando o cursor com a opção de retorno como dicionário   
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)

    for (registro) in cursor:
        print(registro['nome_usuario'] + " - "+ registro['email'])

    cursor.close()


def usuario_checar(user, tipo):
    con = abrir_conexao("localhost", "estudante1", "123", "stats_movie")
    sql = f"SELECT {tipo} FROM usuarios WHERE {tipo}='{user}'"
    # Criando o cursor com a opção de retorno como dicionário   
    cursor = con.cursor(dictionary=True)
    cursor.execute(sql)
    resultado = 0
    for (registro) in cursor:
        if str(registro) != "":
            resultado = registro[f'{tipo}']

    return resultado

def usuario_inserir(nome_usuario, email, senha):
    con = abrir_conexao("localhost", "estudante1", "123", "stats_movie")
    cursor = con.cursor(dictionary=True)
    sql = f"INSERT INTO usuarios (nome_usuario, email, senha) VALUES ('{nome_usuario}', '{email}', '{senha}')"
    cursor.execute(sql)
    con.commit() 
    cursor.close()