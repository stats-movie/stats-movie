import mysql.connector


def abrir_conexao(host, user, passwd, database):
    return mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)

def abrir_conexao_database(host, user, passwd):
    return mysql.connector.connect(host=host, user=user, passwd=passwd)

def fechar_conexao(con):
    con.close
