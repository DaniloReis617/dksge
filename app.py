import streamlit as st
from pages import dashboard_app, clientes_app, vendas_app, estoque_app, funcionarios_app
from utils.auth_utils import login

# Configurações gerais do Streamlit
st.set_page_config(page_title='Gestor Empresarial', layout='wide')

# Função para navegação entre páginas
@st.cache
def get_app_pages():
    return {
        "Dashboard": dashboard_app,
        "Clientes": clientes_app,
        "Vendas": vendas_app,
        "Estoque": estoque_app,
        "Funcionários": funcionarios_app
    }

# Sidebar com navegação entre páginas
def main():
    st.sidebar.title('Menu')
    pages = get_app_pages()
    selection = st.sidebar.radio("Selecione uma opção", list(pages.keys()))

    page = pages[selection]
    page()

if __name__ == '__main__':
    user = login()  # Função de login
    if user:
        main()   # Função principal para execução do app
