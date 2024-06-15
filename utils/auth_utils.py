# utils/auth_utils.py

import sqlite3

# Função para verificar login de usuário
def login_user(username, password):
    conn = sqlite3.connect('DB/loteria.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Função para registrar um novo usuário
def register_user(username, password):
    conn = sqlite3.connect('DB/loteria.db')
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Função para verificar se um usuário já existe pelo username
def check_existing_username(username):
    conn = sqlite3.connect('DB/loteria.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# Função para fazer logout do usuário (limpar a sessão)
def logout_user():
    # Implemente conforme necessário
    pass

# Outras funções de autenticação conforme necessário
