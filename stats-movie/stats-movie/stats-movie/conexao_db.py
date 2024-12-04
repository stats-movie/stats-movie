import mysql.connector


def abrir_conexao(host, user, passwd, database):
    return mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)

def fechar_conexao(con):
    con.close
