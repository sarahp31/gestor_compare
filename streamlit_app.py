import streamlit as st
import pandas as pd

# Configurações básicas do app
st.set_page_config(page_title="Comparador de Gestoras", layout="centered")

# Título da aplicação
st.title("Comparador de Gestoras")

# Upload dos arquivos
st.subheader("Upload de Arquivos Excel")
file1 = st.file_uploader("Arquivo Antigo", type=["xlsx"])
file2 = st.file_uploader("Arquivo Novo", type=["xlsx"])

if file1 and file2:
    try:
        # Carregando os arquivos Excel
        df1 = pd.read_excel(file1, sheet_name='Pág. 2 - PL por Categoria', index_col=None)
        df2 = pd.read_excel(file2, sheet_name='Pág. 2 - PL por Categoria', index_col=None)

        # Removendo as primeiras linhas da tabela (não relevantes)
        df1 = df1.iloc[4:]
        df2 = df2.iloc[4:]

        # Redefinindo o nome das colunas
        df1.columns = df1.iloc[0]
        df1 = df1[1:]

        df2.columns = df2.iloc[0]
        df2 = df2[1:]

        # Acessando o nome dos gestores
        df1_gestoras = df1["Gestor"].tolist()
        df2_gestoras = df2["Gestor"].tolist()

        # Comparando os nomes dos gestores
        novo_gestor = set(set(df2_gestoras) - set(df1_gestoras))
        novo_gestor = {g.strip() for g in novo_gestor}

        # Exibindo os resultados
        st.subheader("Resultados")
        if novo_gestor:
            st.success("Novos Gestores Encontrados:")
            for gestor in novo_gestor:
                st.write(f"- {gestor}")
        else:
            st.info("Nenhum novo gestor encontrado.")

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os arquivos: {str(e)}")

else:
    st.info("Por favor, faça o upload de dois arquivos Excel.")
