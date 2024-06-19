import sqlite3
import os

DB_PATH = "DB/database.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def check_existing_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

def authenticate_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verifica se o usuário existe
    cursor.execute("SELECT * FROM Usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    if not user:
        conn.close()
        return "user_not_found"
    
    # Verifica se a senha está correta
    cursor.execute("SELECT * FROM Usuarios WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        return user
    else:
        return "incorrect_password"

