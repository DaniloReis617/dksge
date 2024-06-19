import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

# Caminho para a pasta 'Extratos'
extrato_folder_path = '/workspaces/dksge/Extratos'

# Função para obter o caminho do arquivo mais recente na pasta 'Extratos'
def get_latest_file_path(folder_path):
    list_of_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    if list_of_files:
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file
    else:
        return None

# Função para renderizar o dashboard
def render_dashboard(username):
    # Configuração inicial
    st.markdown(f"### Olá, {username}! Bem-vindo ao seu Dashboard.")

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

        # Processamento dos dados conforme instruções fornecidas
        df_upload['Tipo Transação'] = df_upload['Tipo Transação'].str.upper()
        df_upload['Entrada'] = df_upload.apply(lambda x: x['Valor'] if x['Tipo Transação'] == 'CRÉDITO' else 0, axis=1)
        df_upload['Saída'] = df_upload.apply(lambda x: x['Valor'] if x['Tipo Transação'] == 'DÉBITO' else 0, axis=1)

                # Extrair o mês da coluna 'Data' e mapear para o nome em português
        df_upload['Mês'] = pd.to_datetime(df_upload['Data'], format='%d/%m/%Y').dt.month.map(meses)

        # Calcular saldo com base nos dados do upload
        df_upload['Saldo'] = df_upload['Entrada'] - df_upload['Saída']

        # Renomear colunas conforme dados fornecidos
        df_upload.rename(columns={'Valor': 'Valor (R$)', 'Tipo': 'Tipo de Transação', 'Data': 'Data da Transação'}, inplace=True)

    # Carregar dados do arquivo mais recente se existir
    latest_file_path = get_latest_file_path(extrato_folder_path)
    if latest_file_path:
        df_latest = pd.read_csv(latest_file_path)
        st.write("Dados carregados do arquivo mais recente:", latest_file_path)
    else:
        df_latest = pd.DataFrame()

    # Mesclar com novos dados se um novo arquivo for carregado
    if uploaded_file is not None and df_latest.empty == False:
        df_new = pd.read_csv(file_path)
        df_merged = pd.concat([df_latest, df_new], ignore_index=True)
    else:
        df_merged = df_upload if uploaded_file is not None else df_latest


        # Mapeamento de número do mês para nome em português
        meses = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }

        col1, col2, col3 = st.columns([3, 3, 3])
        with col1:
            # Exibir resumos financeiros
            st.metric("Entrada", f"R$ {df_merged['Entrada'].sum():,.2f}")
        with col2:
            st.metric("Saída", f"R$ {df_merged['Saída'].sum():,.2f}")
        with col3:
            st.metric("Saldo", f"R$ {df_merged['Saldo'].sum():,.2f}")

        # Gráficos
        st.header("Gráficos")
        
        # Gráfico de barras para Entrada e Saída por mês
        fig, ax = plt.subplots()
        ax.bar(df_merged['Mês'], df_merged['Entrada'], label='Entrada')
        ax.bar(df_merged['Mês'], df_merged['Saída'], label='Saída', bottom=df_merged['Entrada'])
        ax.set_ylabel('Valor (R$)')
        ax.set_xlabel('Mês')
        ax.set_title('Entrada e Saída por Mês (R$)')
        plt.xticks(rotation=90)
        plt.legend()
        st.pyplot(fig)

        # Gráfico de linha para Saldo acumulado por mês
        fig, ax = plt.subplots()
        ax.plot(df_merged['Mês'], df_merged['Saldo'].cumsum(), marker='o', linestyle='-', color='b', label='Saldo acumulado')
        ax.set_ylabel('Valor (R$)')
        ax.set_xlabel('Mês')
        ax.set_title('Saldo Acumulado por Mês (R$)')
        plt.xticks(rotation=90)
        plt.legend()
        st.pyplot(fig)

        with st.container():
            # Tabela Editável
            st.header("Demonstração do Resultado do Exercício (DRE)")
            st.data_editor(data=df_merged)
        

# Executar o dashboard
if __name__ == '__main__':
    # Criar a pasta 'Extratos' se ela não existir
    if not os.path.exists(extrato_folder_path):
        os.makedirs(extrato_folder_path)

    render_dashboard("username")
