# app.py - Arquivo principal
import re
import streamlit as st
from streamlit_option_menu import option_menu  # Importando o módulo de menu
from utils import db_utils, auth_utils
from pages import dashboard  # Importando o módulo do dashboard

# Configuração da página do Streamlit
st.set_page_config(page_title="Dks Soluções", page_icon="📊", layout="wide")

# Estilos CSS para ajustar a aparência da página
st.markdown("""
    <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

# Função principal que controla o fluxo da aplicação
def main():
    # Verificação de login
    if 'username' not in st.session_state:
        st.session_state.username = None
        st.session_state.logged_in = False

    # Se já estiver logado, redireciona para o dashboard
    if st.session_state.logged_in:
        # Mostrar o menu de navegação na barra lateral
        with st.sidebar:
            selected = option_menu(
                menu_title=None,  # Título do menu (pode ser None)
                options=["Dashboard", "Logout"],  # Opções do menu
                icons=["bar-chart", "box-arrow-right"],  # Ícones opcionais para as opções
                menu_icon="cast",  # Ícone do menu
                default_index=0,  # Índice padrão selecionado
                orientation="vertical",  # Orientação do menu (vertical ou horizontal)
                styles={  # Estilos CSS personalizados para o menu
                    "container": {"padding": "0!important", "background-color": "#f0f2f6"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {"font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )
        
        # Redirecionamento com base na opção selecionada
        if selected == "Dashboard":
            dashboard.render_dashboard(st.session_state.username, st.session_state.user_id)

        elif selected == "Logout":
            st.session_state.username = None
            st.session_state.logged_in = False
            st.experimental_rerun()  # Reinicia o aplicativo após logout
        return
    else:
        st.error("Você não está logado. Por favor, faça o login para acessar o dashboard.")

    # Tela de login e registro
    with st.container():
        col1, col2, col3 = st.columns([2, 6, 2])
        with col2:
            # Guias de Registro/Login
            tab1, tab2 = st.tabs(["Login", "Registrar Conta"])
            with tab1:
                username = login()
                if username:
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.experimental_rerun()  # Reinicia o aplicativo após login bem-sucedido
            with tab2:
                if registro():  # Se o cadastro for bem-sucedido
                    st.experimental_rerun()  # Reinicia o aplicativo após registro

# Função para realizar login
def login():
    with st.container():
        with st.form(key='login_form'):
            st.subheader("Login")
            username = st.text_input("Email", placeholder="Digite seu Email")
            # Verifica se o email é válido
            if not re.match(r"[^@]+@[^@]+\.[^@]+", username):
                st.error("Por favor, insira um email válido.")
            password = st.text_input("Senha", placeholder="Digite sua senha", type='password')
            if st.form_submit_button('Entrar'):
                result = auth_utils.login_user(username, password)
                if result == "user_not_found":
                    st.error('Usuário não encontrado.')
                elif result == "incorrect_password":
                    st.error('Senha incorreta.')
                elif result:
                    st.session_state.username = username
                    st.session_state.logged_in = True
                    st.session_state.user_id = result  # Set user_id based on actual user_id retrieval
                    st.success(f'Login realizado com sucesso como {username}!')
                    return username  # Retorna o username se o login for bem-sucedido
                else:
                    st.error('Erro desconhecido. Por favor, tente novamente.')

# Função para realizar registro de novo usuário
def registro():
    with st.container():
        col1, col2, col3 = st.columns([0.5, 8, 0.5])
        with col2:
            st.subheader("Registro")
            with st.form(key='register_form'):
                # Campo para inserir novo email
                new_username = st.text_input("E-mail", placeholder="Digite seu Email")
                # Verifica se o email é válido
                if not re.match(r"[^@]+@[^@]+\.[^@]+", new_username):
                    st.error("Por favor, insira um email válido.")
                # Campo para inserir nova senha
                new_password = st.text_input("Nova Senha", placeholder="Digite sua senha", type='password')
                # Campo para confirmar a nova senha
                confirm_password = st.text_input("Confirme a Nova Senha", placeholder="Digite sua senha novamente", type='password')
                # Verifica se a senha e a confirmação coincidem
                if new_password != confirm_password:
                    st.error("As senhas digitadas não coincidem. Por favor, tente novamente.")
                # Botão para submeter o formulário de registro
                if st.form_submit_button('Criar Conta'):
                    # Verifica se o email já está em uso
                    existing_user = db_utils.check_existing_username(new_username)
                    if existing_user:
                        st.error(f'O email "{new_username}" já está em uso. Por favor, escolha outro.')
                    else:
                        # Registra o usuário se o email não estiver em uso
                        db_utils.register_user(new_username, new_password)
                        st.success(f'Conta registrada com sucesso para {new_username}!')

    return False  # Retorna falso se o formulário não foi submetido

# Executa o aplicativo
if __name__ == "__main__":
    main()
