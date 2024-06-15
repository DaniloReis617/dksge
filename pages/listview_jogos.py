# pages/listview_jogos.py

import streamlit as st

def render_listview_jogos(username):
    
    with st.container():
        col1, col2, col3, col4, col5 = st.columns([6, 1, 1, 1, 1])  # 4 colunas com largura igual
        with col1:
            # Exibir uma mensagem de boas-vindas com o nome do usuário
            st.markdown(f"### Olá, {username}! Bem-vindo ao seu Dashboard.")
        with col2:
            if st.button("Visualizar Registros"): # Adicione um botão ou algum gatilho para navegar para a tela Visualizar_transacao
                st.session_state.exibir_visualizacao = True
                # Exibir a tela de visualização de registros se a variável de estado for True
                if st.session_state.exibir_visualizacao:
                    pass
                    st.experimental_rerun()
                    #ListView_Transacao.tela_visualizar_transacoes()  # Chamar a função para exibir a página Visualizar_transacao
        with col3:
            if st.button("Adicionar Registros"):
                pass
        with col4:
            if st.button("Atualizar Dados"):
                # Chamar a função para recarregar os dados do usuário
                st.experimental_rerun()
        with col5:
            if st.button("Sair"):
                st.session_state.username = None  # Limpar os detalhes do usuário
                st.experimental_rerun()

    # Adicione funcionalidades conforme necessário
