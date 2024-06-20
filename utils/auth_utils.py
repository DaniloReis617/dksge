# utils/auth_utils.py - Módulo para autenticação

import hashlib  # Importa hashlib para hashing de senhas
from utils.db_utils import register_user, authenticate_user  # Importa funções de utilitários de banco de dados

# Função para hashear a senha
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Função para realizar login de usuário
def login_user(username, password):
    hashed_password = hash_password(password)
    user = authenticate_user(username, hashed_password)
    if user:
        return user[0]  # Retorna o ID do usuário (assumindo que é a primeira coluna)
    return None

# Função para registrar novo usuário
def register(username, password):
    hashed_password = hash_password(password)
    register_user(username, hashed_password)
