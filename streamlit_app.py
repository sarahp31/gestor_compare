import streamlit as st
import pandas as pd

# Configurações básicas do app
st.set_page_config(page_title="Novas Gestoras", layout="centered")

# Título da aplicação
st.title("Novas Gestoras")

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
        df1.columns = df1.iloc[0].str.replace("\n", "").str.strip()
        df1 = df1[1:]

        df2.columns = df2.iloc[0].str.replace("\n", "").str.strip()
        df2 = df2[1:]

        # Limpando valores nulos nas colunas de interesse
        df1 = df1[["Gestor", "Total"]].dropna()
        df2 = df2[["Gestor", "Total"]].dropna()

        # Garantindo que a coluna "Total" seja numérica
        df1["Total"] = pd.to_numeric(df1["Total"], errors="coerce")
        df2["Total"] = pd.to_numeric(df2["Total"], errors="coerce")

        # Criando dicionários de gestor para total
        df1_dict = dict(zip(df1["Gestor"].str.strip(), df1["Total"]))
        df2_dict = dict(zip(df2["Gestor"].str.strip(), df2["Total"]))

        # Comparando os nomes dos gestores e valores associados
        novo_gestor = {gestor: df2_dict[gestor] for gestor in df2_dict if gestor not in df1_dict}

        # Ordenando os resultados pelo valor do Total (decrescente)
        novo_gestor = dict(sorted(novo_gestor.items(), key=lambda item: item[1], reverse=True))

        # Exibindo os resultados
        st.subheader("Resultados")
        if novo_gestor:
            st.success("Novas Gestoras Encontradas:")

            # Criando um DataFrame para exibir os resultados
            resultados_df = pd.DataFrame(
                [{"Gestor": gestor, "AUM": total} for gestor, total in novo_gestor.items()]
            )

            # Ajustando o indice da tabela
            resultados_df.index = range(1, len(resultados_df) + 1)

            # Exibindo os resultados como uma tabela no Streamlit
            st.table(resultados_df.style.format({"AUM": "R$ {:,.2f}"}))
        else:
            st.info("Nenhum novo gestor encontrado.")

    except Exception as e:
        st.error(f"Ocorreu um erro ao processar os arquivos: {str(e)}")

else:
    st.info("Por favor, faça o upload de dois arquivos Excel.")
