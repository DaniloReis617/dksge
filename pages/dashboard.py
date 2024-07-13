import streamlit as st
import pandas as pd
import os
from datetime import datetime
import plotly.graph_objects as go
from utils.db_utils import add_data_to_extrato_table, get_extrato_data, add_new_transaction, edit_transaction, delete_transaction

# Caminho para a pasta 'Extratos'
extrato_folder_path = 'Extratos'

# Função para obter o caminho do arquivo mais recente na pasta 'Extratos'
def get_latest_file_path(folder_path):
    list_of_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    return None

@st.experimental_dialog("Adicionar Transação")
# Função para adicionar uma nova transação
def add_transaction(user_id):
    with st.form(key='new_transaction_form'):
        st.subheader('Nova Transação')
        data_da_transacao = st.date_input("Data da Transação", key='new_date')
        transacao = st.text_input("Transação", key='new_transacao')
        tipo_transacao = st.selectbox("Tipo de Transação", ['CRÉDITO', 'DÉBITO'], key='new_tipo_transacao')
        identificacao = st.text_input("Identificação", key='new_identificacao')
        valor = st.number_input("Valor", min_value=0.0, step=0.01, key='new_valor')
        entrada = valor if tipo_transacao == 'CRÉDITO' else 0
        saida = valor if tipo_transacao == 'DÉBITO' else 0
        mes = data_da_transacao.strftime('%B')
        saldo = entrada - saida

        if st.form_submit_button('Adicionar'):
            add_new_transaction(user_id, data_da_transacao, transacao, tipo_transacao, identificacao, valor, entrada, saida, mes, saldo)
            st.success('Nova transação adicionada com sucesso.')
            st.experimental_rerun()

# Função para renderizar o dashboard
def render_dashboard(username, user_id):
    col1, col2, col3, col4, col5 = st.columns([6, 1, 1, 1, 1])  # 4 colunas com largura igual
    with col1:
        # Configuração inicial
        st.markdown(f"### Olá, {username}! Bem-vindo ao seu Dashboard.")

    with col3:
        if st.button("Adicionar Transação"):
            add_transaction(user_id)

    with col4:
        if st.button("Atualizar Dados"):
            # Chamar a função para recarregar os dados do usuário
            df_extrato = get_extrato_data(user_id)
            st.success('Dados atualizados com sucesso.')

    with col5:
        if st.button("Sair"):
            st.session_state.username = None
            st.session_state.logged_in = False
            st.experimental_rerun()  # Reinicia o aplicativo após logout

    # Buscar dados da tabela Extrato
    df_extrato = get_extrato_data(user_id)

    # Verificar se as colunas necessárias estão presentes no DataFrame
    required_columns = ['Mes', 'Tipo_Transacao', 'Valor', 'Saldo']
    if not all(col in df_extrato.columns for col in required_columns):
        st.error("Os dados recuperados do banco de dados não contêm todas as colunas necessárias.")
        return

    # Cards
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        st.metric("Entrada", f"R$ {df_extrato[df_extrato['Tipo_Transacao'] == 'CRÉDITO']['Valor'].sum():,.2f}")
    with col2:
        st.metric("Saída", f"R$ {df_extrato[df_extrato['Tipo_Transacao'] == 'DÉBITO']['Valor'].sum():,.2f}")
    with col3:
        st.metric("Saldo", f"R$ {df_extrato['Saldo'].sum():,.2f}")

    # Gráficos
    st.header("Gráficos")

    # Verificar se df_extrato não está vazio antes de plotar os gráficos
    if not df_extrato.empty:
        # Gráfico de colunas para Entrada e Saída por mês
        fig_colunas = go.Figure()

        fig_colunas.add_trace(go.Bar(
            x=df_extrato[df_extrato['Tipo_Transacao'] == 'CRÉDITO']['Mes'],
            y=df_extrato[df_extrato['Tipo_Transacao'] == 'CRÉDITO']['Valor'],
            name='Crédito',
            marker_color='rgb(55, 83, 109)',
            offsetgroup=0
        ))

        fig_colunas.add_trace(go.Bar(
            x=df_extrato[df_extrato['Tipo_Transacao'] == 'DÉBITO']['Mes'],
            y=df_extrato[df_extrato['Tipo_Transacao'] == 'DÉBITO']['Valor'],
            name='Débito',
            marker_color='rgb(26, 118, 255)',
            offsetgroup=1
        ))

        fig_colunas.update_layout(
            title='Entrada e Saída por Mês (R$)',
            xaxis_tickfont_size=14,
            yaxis=dict(title='Valor (R$)'),
            barmode='group',
            legend=dict(title='Tipo de Transação', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(fig_colunas)

        # Gráfico de linha para Saldo acumulado por mês
        fig_linha = go.Figure()

        fig_linha.add_trace(go.Scatter(
            x=df_extrato['Mes'],
            y=df_extrato['Saldo'].cumsum(),
            mode='lines+markers',
            name='Saldo acumulado',
            line=dict(color='rgb(55, 83, 109)', width=2)
        ))

        fig_linha.update_layout(
            title='Saldo Acumulado por Mês (R$)',
            xaxis_tickfont_size=14,
            yaxis=dict(title='Saldo (R$)'),
            legend=dict(title='Tipo de Transação', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
            margin=dict(l=20, r=20, t=60, b=20),
        )

        st.plotly_chart(fig_linha)

    else:
        st.warning("Não há dados disponíveis para plotar os gráficos.")

    with st.container():
        col1, col2, col3 = st.columns([0.5, 9, 0.5])
        with col2:
            # Exibir e editar transações existentes
            st.header("Transações Existentes")
            df_extrato = get_extrato_data(user_id)
            st.write(df_extrato)
            # Editor de dados para Demonstração do Resultado do Exercício (DRE)
            st.header("Demonstração do Resultado do Exercício (DRE)")

            edited_df = st.data_editor(
                df_extrato,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "ID_Transacao": st.column_config.NumberColumn("ID_Transacao",disabled=True),
                    "ID_User": None,  # Ocultar coluna de ID do usuário
                    "Data_da_Transacao": "Data",
                    "Transacao": "Descrição",
                    "Tipo_Transacao": "Tipo de Transação",
                    "Identificacao": "Identificação",
                    "Valor (R$)": st.column_config.NumberColumn("Valor (R$)", format="R$ %.2f"),
                    "Entrada": "Entrada",
                    "Saida": "Saída",
                    "Mes": "Mês",
                    "Saldo": st.column_config.NumberColumn("Saldo", format="R$ %.2f")
                }
            )

            # Função para lidar com edições de transações
            def handle_edit(edited_df, original_df):
                # Iterar pelas linhas do dataframe editado
                for index, row in edited_df.iterrows():
                    # Verificar se a linha é uma nova entrada
                    if pd.isna(row["ID_Transacao"]):
                        add_new_transaction(
                            user_id=user_id,
                            data_da_transacao=row["Data_da_Transacao"],
                            transacao=row["Transacao"],
                            tipo_transacao=row["Tipo_Transacao"],
                            identificacao=row["Identificacao"],
                            valor=row["Valor (R$)"],
                            entrada=row["Entrada"],
                            saida=row["Saida"],
                            mes=row["Mes"],
                            saldo=row["Saldo"]
                        )
                        st.success(f"Nova transação adicionada com sucesso.")
                    else:
                        # Verificar se a linha foi editada
                        original_row = original_df.loc[original_df["ID_Transacao"] == row["ID_Transacao"]]
                        if not row.equals(original_row.iloc[0]):
                            edit_transaction(
                                id_transacao=row["ID_Transacao"],
                                data_da_transacao=row["Data_da_Transacao"],
                                transacao=row["Transacao"],
                                tipo_transacao=row["Tipo_Transacao"],
                                identificacao=row["Identificacao"],
                                valor=row["Valor (R$)"],
                                entrada=row["Entrada"],
                                saida=row["Saida"],
                                mes=row["Mes"],
                                saldo=row["Saldo"]
                            )
                            st.success(f"Transação {row['ID_Transacao']} atualizada com sucesso.")

                # Verificar se alguma linha foi excluída
                edited_ids = set(edited_df["ID_Transacao"].dropna())
                original_ids = set(original_df["ID_Transacao"].dropna())
                deleted_ids = original_ids - edited_ids
                for deleted_id in deleted_ids:
                    delete_transaction(deleted_id)
                    st.success(f"Transação {deleted_id} excluída com sucesso.")

            if st.button('Salvar Edições'):
                handle_edit(edited_df, df_extrato)
                st.experimental_rerun()

            # Formulário para excluir transações
            with st.form(key='delete_transaction_form'):
                st.subheader('Excluir Transação')
                id_transacao = st.number_input("ID da Transação", min_value=1, step=1, key='delete_id')
                if st.form_submit_button('Excluir'):
                    delete_transaction(id_transacao)
                    st.success(f"Transação {id_transacao} excluída com sucesso.")
                    st.experimental_rerun()
