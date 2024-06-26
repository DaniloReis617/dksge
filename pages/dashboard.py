import streamlit as st
import pandas as pd
import os
from datetime import datetime
import seaborn as sns  # Importar seaborn para melhorar o estilo dos gráficos
import matplotlib.pyplot as plt
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

# Função para renderizar o dashboard
def render_dashboard(username, user_id):
    col1, col2, col3, col4, col5 = st.columns([6, 1, 1, 1, 1])  # 4 colunas com largura igual
    with col1:
        # Configuração inicial
        st.markdown(f"### Olá, {username}! Bem-vindo ao seu Dashboard.")

    with col3:
        if st.button("Adicionar Transação"):
            # Exibir um formulário para adicionar uma nova transação
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
    required_columns = ['Mes', 'Tipo_Transacao', 'Entrada', 'Saida', 'Saldo']
    if not all(col in df_extrato.columns for col in required_columns):
        st.error("Os dados recuperados do banco de dados não contêm todas as colunas necessárias.")
        return

    # Cards
    col1, col2, col3 = st.columns([3, 3, 3])
    with col1:
        st.metric("Entrada", f"R$ {df_extrato['Entrada'].sum():,.2f}")
    with col2:
        st.metric("Saída", f"R$ {df_extrato['Saida'].sum():,.2f}")
    with col3:
        st.metric("Saldo", f"R$ {df_extrato['Saldo'].sum():,.2f}")

    # Gráficos
    st.header("Gráficos")

    # Estilo Seaborn
    sns.set_theme(style="whitegrid", font_scale=1.2, palette="pastel")

    # Gráfico de histograma para Entrada e Saída por mês
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data=df_extrato, x='Mes', hue='Tipo_Transacao', multiple='stack', edgecolor='white', alpha=0.7, ax=ax)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Valor (R$)')
    ax.set_title('Entrada e Saída por Mês (R$)')
    plt.xticks(rotation=90)
    ax.legend(title='Tipo de Transação', loc='upper right', bbox_to_anchor=(1.05, 1))
    st.pyplot(fig)

    # Gráfico de linha para Saldo acumulado por mês
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=df_extrato, x='Mes', y=df_extrato['Saldo'].cumsum(), marker='o', linestyle='-', color='#3498db', label='Saldo acumulado', ax=ax)
    ax.set_xlabel('Mês')
    ax.set_ylabel('Valor (R$)')
    ax.set_title('Saldo Acumulado por Mês (R$)')
    plt.xticks(rotation=90)
    ax.legend(loc='upper right', bbox_to_anchor=(1.05, 1))
    st.pyplot(fig)

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
                    "Valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
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
                            valor=row["Valor"],
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
                                valor=row["Valor"],
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
                if st.form_submit_button('Confirmar Exclusão'):
                    delete_transaction(id_transacao)
                    st.success('Transação excluída com sucesso.')

    # Upload do arquivo CSV
    uploaded_file = st.file_uploader("Upload do Extrato Bancário", type="csv")
    
    # Variável para armazenar o caminho do arquivo carregado
    file_path = None

    if uploaded_file is not None:
        # Contar o número de arquivos na pasta 'Extratos'
        num_files = len([name for name in os.listdir(extrato_folder_path) if os.path.isfile(os.path.join(extrato_folder_path, name))])

        # Gerar o nome do arquivo com o formato desejado
        today = datetime.now().strftime('%Y-%m-%d')
        file_name = f"Extrato_{num_files}_{today}.csv"

        # Salvar o arquivo na pasta 'Extratos', substituindo se já existir
        file_path = os.path.join(extrato_folder_path, file_name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("Arquivo salvo com o nome: " + file_name)

        # Ler arquivo CSV da pasta 'Extratos' e exibir os dados
        df_upload = pd.read_csv(file_path)

        # Verificar se as colunas esperadas estão presentes no DataFrame
        expected_columns = ['Data', 'Transação', 'Tipo Transação', 'Identificação', 'Valor']
        if all(col in df_upload.columns for col in expected_columns):
            # Processamento dos dados conforme instruções fornecidas
            df_upload['Tipo Transação'] = df_upload['Tipo Transação'].str.upper()
            df_upload['Entrada'] = df_upload.apply(lambda x: x['Valor'] if x['Tipo Transação'] == 'CRÉDITO' else 0, axis=1)
            df_upload['Saida'] = df_upload.apply(lambda x: x['Valor'] if x['Tipo Transação'] == 'DÉBITO' else 0, axis=1)

            # Mapeamento de número do mês para nome em português
            meses = {
                1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
                5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
                9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
            }

            # Extrair o mês da coluna 'Data' e mapear para o nome em português
            df_upload['Mes'] = pd.to_datetime(df_upload['Data'], format='%d/%m/%Y').dt.month.map(meses)

            # Calcular saldo com base nos dados do upload
            df_upload['Saldo'] = df_upload['Entrada'] - df_upload['Saida']

            # Renomear colunas conforme dados fornecidos
            df_upload.rename(columns={'Data': 'Data_da_Transacao', 'Transação': 'Transacao', 'Identificação': 'Identificacao', 'Valor': 'Valor (R$)', 'Tipo Transação': 'Tipo_Transacao'}, inplace=True)

            # Adicionar user_id à DataFrame antes de inserir no banco de dados
            df_upload['ID_User'] = user_id

            # Adicionar dados à tabela Extrato
            add_data_to_extrato_table(df_upload, user_id)

            # Buscar dados da tabelaExtrato
            df_extrato = get_extrato_data(user_id)

            # Verificar se as colunas necessárias estão presentes no DataFrame
            required_columns = ['Mes', 'Tipo_Transacao', 'Entrada', 'Saida', 'Saldo']
            if not all(col in df_extrato.columns for col in required_columns):
                st.error("Os dados recuperados do banco de dados não contêm todas as colunas necessárias.")
                return

            # Delete the uploaded CSV file
            if os.path.exists(file_path):
                os.remove(file_path)
                st.write(f"Arquivo '{file_name}' excluído com sucesso.")
            else:
                st.write(f"Arquivo '{file_name}' não encontrado.")

# Executar o dashboard
if __name__ == '__main__':
    # Criar a pasta 'Extratos' se ela não existir
    if not os.path.exists(extrato_folder_path):
        os.makedirs(extrato_folder_path)

    username = "username"
    user_id = 1  # Substitua pelo ID do usuário real
    render_dashboard(username, user_id)