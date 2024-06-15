import hashlib
from datetime import datetime
import pandas as pd
import sqlite3
import streamlit as st
from utils.db_utils import log_usuario  # Ajustar o caminho de importação
from utils.models import User_Cliente

def login():
    with st.container():
        col1, col2, col3 = st.columns([0.5, 9, 0.5])
        with col2:
            st.subheader("Login")
            with st.form(key="form_login", clear_on_submit=True):
                email = st.text_input("Usuário", placeholder="Digite seu Email")
                password = st.text_input("Senha", type="password", placeholder="Digite sua senha")

                if st.form_submit_button("Entrar"):
                    try:
                        user_cliente = User_Cliente("", "", email, password,"")
                        User_Cliente_logado = log_usuario(user_cliente)
                        if User_Cliente_logado:
                            st.success("Login realizado com sucesso!")
                            # Redirecionar para uma página de dashboard ou outra ação
                            st.write("Você está logado!")
                            return User_Cliente_logado  # Retorna os detalhes do usuário logado
                        else:
                            st.error("Usuário ou senha incorretos.")
                    except Exception as e:
                        st.error(f"Ocorreu um erro ao tentar fazer login: {str(e)}")
            return None  # Retorna None se o login falhar