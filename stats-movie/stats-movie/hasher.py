from argon2 import PasswordHasher

def senha_hash(hash_text):
    ph = PasswordHasher()
    hash = ph.hash(hash_text)
    return hash

def verifica_senha(senha, hash_text):
    ph = PasswordHasher()
    try:
        resultado = ph.verify(hash_text, senha)
        return resultado
    except:
        return False