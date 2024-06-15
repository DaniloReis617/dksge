import hashlib
from datetime import datetime
import pandas as pd
import sqlite3
from utils.models import User_Cliente

# Conexão com o Banco de Dados
def create_connection_db():
    conn = sqlite3.connect('DB/database.db') 
    cursor = conn.cursor()
    return conn, cursor

# Funções CRUD para a Tabela Usuarios
# Cadastro de Usuário
def cadastrar_usuario(username, email, password, profile):
    conn, cursor = create_connection_db()
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute("""
            INSERT INTO Usuarios (username, password, email, profile)
            VALUES (?, ?, ?, ?)
        """, (username, hashed_password, email, profile))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar o usuário: {str(e)}")
    finally:
        conn.close()

# Verificação de E-mail Existente
def verificar_email_existente(email):
    conn, cursor = create_connection_db()
    cursor.execute("SELECT * FROM Usuarios WHERE LOWER(email) = LOWER(?)", (email,))
    row = cursor.fetchone()
    conn.close()
    return row is not None

def log_usuario(User_Cliente):
    # Abrir a conexão com o banco de dados
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    # Hash da senha
    senha_hash = hashlib.sha256(User_Cliente.senha.encode()).hexdigest()
    # Consulta SQL para verificar se o usuário existe no banco de dados
    query = f"""
    SELECT * FROM usuarios WHERE email = ? AND senha = ?;
    """
    # Executar a consulta SQL
    cursor.execute(query, (User_Cliente.email, senha_hash))
    # Obter o resultado da consulta
    resultado = cursor.fetchone()
    # Fechar a conexão com o banco de dados
    conn.close()
    # Verificar se o usuário existe no banco de dados
    if resultado:
        # Retornar o objeto User_Cliente com os dados do usuário
        return User_Cliente(*resultado)
    else:
        # Retornar None se o usuário não existir no banco de dados
        return None

# Atualização de Usuário
def atualizar_usuario(user_id, updates):
    conn, cursor = create_connection_db()
    try:
        set_string = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(user_id)
        cursor.execute(f"UPDATE Usuarios SET {set_string} WHERE id = ?", values)
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar atualizar o usuário: {str(e)}")
    finally:
        conn.close()

# Exclusão de Usuário
def deletar_usuario(user_id):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("DELETE FROM Usuarios WHERE id = ?", (user_id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar excluir o usuário: {str(e)}")
    finally:
        conn.close()

# Funções CRUD para a Tabela Clientes
# Cadastro de Cliente
def cadastrar_cliente(nome_cliente, contato, email, endereco):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("""
            INSERT INTO Clientes (nome_cliente, contato, email, endereco)
            VALUES (?, ?, ?, ?)
        """, (nome_cliente, contato, email, endereco))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar o cliente: {str(e)}")
    finally:
        conn.close()

# Atualização de Cliente
def atualizar_cliente(cliente_id, updates):
    conn, cursor = create_connection_db()
    try:
        set_string = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(cliente_id)
        cursor.execute(f"UPDATE Clientes SET {set_string} WHERE id_cliente = ?", values)
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar atualizar o cliente: {str(e)}")
    finally:
        conn.close()

# Exclusão de Cliente
def deletar_cliente(cliente_id):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("DELETE FROM Clientes WHERE id_cliente = ?", (cliente_id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar excluir o cliente: {str(e)}")
    finally:
        conn.close()

# Funções CRUD para a Tabela Financeira
# Cadastro de Transação Financeira
def cadastrar_transacao(tipo_transacao, categoria_transacao, valor, moeda_transacao, metodo_pagamento, notas):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("""
            INSERT INTO Financeira (tipo_transacao, categoria_transacao, valor, moeda_transacao, metodo_pagamento, notas)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (tipo_transacao, categoria_transacao, valor, moeda_transacao, metodo_pagamento, notas))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar a transação: {str(e)}")
    finally:
        conn.close()

# Atualização de Transação Financeira
def atualizar_transacao(transacao_id, updates):
    conn, cursor = create_connection_db()
    try:
        set_string = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(transacao_id)
        cursor.execute(f"UPDATE Financeira SET {set_string} WHERE id_transacao = ?", values)
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar atualizar a transação: {str(e)}")
    finally:
        conn.close()

# Exclusão de Transação Financeira
def deletar_transacao(transacao_id):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("DELETE FROM Financeira WHERE id_transacao = ?", (transacao_id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar excluir a transação: {str(e)}")
    finally:
        conn.close()

# Funções CRUD para a Tabela Estoque
# Cadastro de Produto
def cadastrar_produto(nome_produto, descricao_produto, quantidade_estoque, preco_custo, preco_venda, fornecedor):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("""
            INSERT INTO Estoque (nome_produto, descricao_produto, quantidade_estoque, preco_custo, preco_venda, fornecedor)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nome_produto, descricao_produto, quantidade_estoque, preco_custo, preco_venda, fornecedor))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar o produto: {str(e)}")
    finally:
        conn.close()

# Atualização de Produto
def atualizar_produto(produto_id, updates):
    conn, cursor = create_connection_db()
    try:
        set_string = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(produto_id)
        cursor.execute(f"UPDATE Estoque SET {set_string} WHERE id_produto = ?", values)
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar atualizar o produto: {str(e)}")
    finally:
        conn.close()

# Exclusão de Produto
def deletar_produto(produto_id):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("DELETE FROM Estoque WHERE id_produto = ?", (produto_id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar excluir o produto: {str(e)}")
    finally:
        conn.close()

# Funções CRUD para a Tabela Vendas
# Cadastro de Venda
def cadastrar_venda(id_cliente, id_produto, quantidade, preco_unitario, total, metodo_pagamento, moeda):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("""
            INSERT INTO Vendas (id_cliente, id_produto, quantidade, preco_unitario, total, metodo_pagamento, moeda)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_cliente, id_produto, quantidade, preco_unitario, total, metodo_pagamento, moeda))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar a venda: {str(e)}")
    finally:
        conn.close()

# Atualização de Venda
def atualizar_venda(venda_id, updates):
    conn, cursor = create_connection_db()
    try:
        set_string = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(venda_id)
        cursor.execute(f"UPDATE Vendas SET {set_string} WHERE id_venda = ?", values)
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar atualizar a venda: {str(e)}")
    finally:
        conn.close()
        
# Exclusão de Venda
def deletar_venda(venda_id):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("DELETE FROM Vendas WHERE id_venda = ?", (venda_id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar excluir a venda: {str(e)}")
    finally:
        conn.close()

# Funções CRUD para a Tabela Funcionarios
# Cadastro de Funcionário
def cadastrar_funcionario(nome_funcionario, cargo, salario, departamento, contato):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("""
            INSERT INTO Funcionarios (nome_funcionario, cargo, salario, departamento, contato)
            VALUES (?, ?, ?, ?, ?)
        """, (nome_funcionario, cargo, salario, departamento, contato))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar o funcionário: {str(e)}")
    finally:
        conn.close()

# Atualização de Funcionário
def atualizar_funcionario(funcionario_id, updates):
    conn, cursor = create_connection_db()
    try:
        set_string = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(funcionario_id)
        cursor.execute(f"UPDATE Funcionarios SET {set_string} WHERE id_funcionario = ?", values)
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar atualizar o funcionário: {str(e)}")
    finally:
        conn.close()

# Exclusão de Funcionário
def deletar_funcionario(funcionario_id):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("DELETE FROM Funcionarios WHERE id_funcionario = ?", (funcionario_id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar excluir o funcionário: {str(e)}")
    finally:
        conn.close()

#Funções CRUD para a Tabela Vendas
# Cadastro de Venda
def cadastrar_venda(id_cliente, id_produto, quantidade, preco_unitario, total, metodo_pagamento, moeda):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("""
            INSERT INTO Vendas (id_cliente, id_produto, quantidade, preco_unitario, total, metodo_pagamento, moeda)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id_cliente, id_produto, quantidade, preco_unitario, total, metodo_pagamento, moeda))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar cadastrar a venda: {str(e)}")
    finally:
        conn.close()

# Atualização de Venda
def atualizar_venda(venda_id, updates):
    conn, cursor = create_connection_db()
    try:
        set_string = ', '.join([f"{key} = ?" for key in updates.keys()])
        values = list(updates.values())
        values.append(venda_id)
        cursor.execute(f"UPDATE Vendas SET {set_string} WHERE id_venda = ?", values)
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar atualizar a venda: {str(e)}")
    finally:
        conn.close()

# Exclusão de Venda
def deletar_venda(venda_id):
    conn, cursor = create_connection_db()
    try:
        cursor.execute("DELETE FROM Vendas WHERE id_venda = ?", (venda_id,))
        conn.commit()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar excluir a venda: {str(e)}")
    finally:
        conn.close()