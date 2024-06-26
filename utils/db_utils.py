# utils/db_utils.py - Módulo para utilitários de banco de dados

import sqlite3  # Importa sqlite3 para interação com o banco de dados SQLite
import os  # Importa os para operações de sistema
import pandas as pd  # Importa pandas para manipulação de dados

DB_PATH = "DB/database.db"  # Caminho para o banco de dados

# Função para obter a conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Função para registrar novo usuário
def register_user(username, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Usuarios (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

# Função para verificar se o username já existe
def check_existing_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuarios WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    return user

# Função para autenticar usuário
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

# Função para adicionar dados na tabela Extrato
def add_data_to_extrato_table(df_upload, user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Inserir os dados do arquivo CSV na tabela Extrato
    for _, row in df_upload.iterrows():
        cursor.execute(
            """
            INSERT INTO Extrato (ID_User, Data_da_Transacao, Transacao, Tipo_Transacao, Identificacao, Valor, Entrada, Saida, Mes, Saldo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                row['Data_da_Transacao'],
                row['Transacao'],
                row['Tipo_Transacao'],
                row['Identificacao'],
                row['Valor (R$)'],
                row['Entrada'],
                row['Saida'],
                row['Mes'],
                row['Saldo']
            )
        )
    
    conn.commit()
    conn.close()

# Função para obter os dados do extrato
def get_extrato_data(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Extrato WHERE ID_User = ?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    
    # Converter os dados em um DataFrame
    df = pd.DataFrame(rows, columns=['ID_Transacao', 'ID_User', 'Data_da_Transacao', 'Transacao', 'Tipo_Transacao', 'Identificacao', 'Valor', 'Entrada', 'Saida', 'Mes', 'Saldo'])
    return df

# Função para adicionar uma nova transação
def add_new_transaction(user_id, data_da_transacao, transacao, tipo_transacao, identificacao, valor, entrada, saida, mes, saldo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Extrato (ID_User, Data_da_Transacao, Transacao, Tipo_Transacao, Identificacao, Valor, Entrada, Saida, Mes, Saldo)
        VALUES (?,?,?,?,?,?,?,?,?,?)
        """,
        (
            user_id,
            data_da_transacao,
            transacao,
            tipo_transacao,
            identificacao,
            valor,
            entrada,
            saida,
            mes,
            saldo
        )
    )
    conn.commit()
    conn.close()

# Função para editar uma transação
def edit_transaction(id_transacao, data_da_transacao, transacao, tipo_transacao, identificacao, valor, entrada, saida, mes, saldo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Extrato SET
            Data_da_Transacao =?,
            Transacao =?,
            Tipo_Transacao =?,
            Identificacao =?,
            Valor =?,
            Entrada =?,
            Saida =?,
            Mes =?,
            Saldo =?
        WHERE ID_Transacao =?
        """,
        (
            data_da_transacao,
            transacao,
            tipo_transacao,
            identificacao,
            valor,
            entrada,
            saida,
            mes,
            saldo,
            id_transacao
        )
    )
    conn.commit()
    conn.close()

# Função para deletar uma transação
def delete_transaction(id_transacao):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Extrato WHERE ID_Transacao =?", (id_transacao,))
    conn.commit()
    conn.close()