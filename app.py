from os import write
import re
import streamlit as st
from utils import db_utils, auth_utils
from pages import dashboard, cadastro_jogos, listview_jogos

st.set_page_config(page_title="Minhas Apostas", page_icon=":game_die:", layout="wide")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
       .reportview-container.main.block-container{padding-top: 0rem;}
       .reportview-container.main footer {visibility: hidden;}
       .sidebar.sidebar-content {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Interface do aplicativo
def main():

    # Verificação de login
    if 'username' not in st.session_state:
        st.session_state.username = None
        st.session_state.logged_in = False

    # Se já estiver logado, redireciona para o dashboard
    if st.session_state.logged_in:
        dashboard.render_dashboard(st.session_state.username)
        return

    with st.container():
        col1, col2, col3 = st.columns([2,6,2])
        with col2:
            # Guias de Registro/Login
            tab1, tab2 = st.tabs(["Login", "Registrar Conta"])
            with tab1:
                username = login()
                if username:
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.experimental_rerun()  # Recarrega o aplicativo
            with tab2:
                if registro():  # Se o cadastro for bem-sucedido
                    st.experimental_rerun()  # Recarrega o aplicativo


def login():
    with st.container():  
        with st.form(key='login_form'):
            st.subheader("Login")
            username = st.text_input("Email", placeholder="Digite seu Email")
            # Verifica se o novo usuário é um email válido
            if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
                st.error("Por favor, insira um email válido.")
            password = st.text_input("Senha", placeholder="Digite sua senha", type='password')
            if st.form_submit_button('Entrar'):
                user = auth_utils.login_user(username, password)
                if user:
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.success(f'Login realizado com sucesso como {username}!')
                    return username  # Retorna o username se o login for bem-sucedido
                else:
                    st.error('Usuário ou senha incorretos.')


# Defina a função registro()
def registro():
    with st.container():
        col1, col2, col3 = st.columns([0.5, 8, 0.5])
        with col2:
            st.subheader("Registro")
            with st.form(key='register_form'):
                # Campo para inserir o novo usuário (email)
                new_username = st.text_input("E-mail", placeholder="Digite seu Email")                
                # Verifica se o novo usuário é um email válido
                if not re.match(r"[^@]+@[^@]+\.[^@]+", new_username):
                    st.error("Por favor, insira um email válido.")                
                # Campo para inserir a nova senha
                new_password = st.text_input("Nova Senha", placeholder="Digite sua senha", type='password')                
                # Campo para confirmar a nova senha
                confirm_password = st.text_input("Confirme a Nova Senha", placeholder="Digite sua senha novamente", type='password')                
                # Verifica se a senha e a confirmação de senha coincidem
                if new_password != confirm_password:
                    st.error("As senhas digitadas não coincidem. Por favor, tente novamente.")                
                # Botão para submeter o formulário de registro
                if st.form_submit_button('Criar Conta'):
                    # Verificar se o email já está em uso
                    existing_user = db_utils.check_existing_username(new_username)
                    if existing_user:
                        st.error(f'O email "{new_username}" já está em uso. Por favor, escolha outro.')
                    else:
                        # Registra o usuário apenas se não existir
                        db_utils.register_user(new_username, new_password)
                        st.success(f'Conta registrada com sucesso para {new_username}!')

    return False  # Retorna falso se o formulário não foi submetido


if __name__ == "__main__":
    main()
