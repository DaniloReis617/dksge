# utils/db_utils.py

import sqlite3

# Função para conectar ao banco de dados
def connect_db():
    conn = sqlite3.connect('DB/loteria.db')
    return conn

# Função para registrar novo usuário
def register_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Função para verificar se um usuário já existe pelo username
def check_existing_username(username):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# Função para buscar informações de um usuário pelo username
def get_user_by_username(username):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return user

# Função para criar um novo jogo para um usuário
def create_jogo(usuario_id, numeros_jogados, resultado):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO jogos (usuario_id, numeros_jogados, resultado) VALUES (?, ?, ?)", (usuario_id, numeros_jogados, resultado))
    conn.commit()
    conn.close()

# Função para obter todos os jogos de um usuário
def get_jogos_by_user(usuario_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM jogos WHERE usuario_id=?", (usuario_id,))
    jogos = c.fetchall()
    conn.close()
    return jogos

# Função para registrar um registro no backlog (simulação de jogo, por exemplo)
def register_backlog(usuario_id, numeros_simulados):
    conn = connect_db()
    c = conn.cursor()
    c.execute("INSERT INTO backlog (usuario_id, numeros_simulados) VALUES (?, ?)", (usuario_id, numeros_simulados))
    conn.commit()
    conn.close()

# Função para obter todos os registros do backlog de um usuário
def get_backlog_by_user(usuario_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM backlog WHERE usuario_id=?", (usuario_id,))
    backlog = c.fetchall()
    conn.close()
    return backlog

# Função para obter os números que mais saíram nos jogos anteriores
def get_numeros_mais_sairam():
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT resultado, COUNT(*) AS total FROM jogos GROUP BY resultado ORDER BY total DESC LIMIT 10")
    numeros_mais_sairam = c.fetchall()
    conn.close()
    return numeros_mais_sairam
