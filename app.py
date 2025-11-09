# Lista das coisas que estão sendo importadas

import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from wokwi_client import WokwiClientSync
import time
import os

# Primeira parte: Análise de dados de dataset de Iris

st.subheader("Previsão de tipo de Íris de acordo com parâmetros, baseando-se em um dataset")

df = pd.read_csv("iris.csv")

# Aqui é a separação dos "objetos" que analisamos, no caso as partes das Iris, seguido pelo fit do modelo
# LabelEncoder se faz necessário para que o sklearn aceite strings, por isso antes quebrou

x = df[["Comprimento_Sepala", "Largura_Sepala", "Comprimento_Petala", "Largura_Petala"]]
y = df["Especie"]

florzinha = LabelEncoder()
y_flor = florzinha.fit_transform(y)

x_treino, x_teste, y_treino, y_teste = train_test_split(
    x, y_flor, test_size=0.2, random_state=7)

PImodelo= LogisticRegression(max_iter=300, random_state=7) # Escolhi o Random State como 7 porque é o número do grupo
PImodelo.fit(x_treino,y_treino)

# Embaixo é a parte que aparece visível no website, as caixas pra preencher etc

st.divider()

Comprimento_Sepala = st.number_input("Digite o comprimento da sépala em CM", 0.1, 8.0, 0.1)
Largura_Sepala = st.number_input("Digite a largura da sépala em CM", 0.1, 5.0, 0.1)
Comprimento_Petala = st.number_input("Digite o comprimento das pétalas em CM", 0.1, 7.0, 0.1)
Largura_Petala = st.number_input("Digite a largura das pétalas em CM", 0.1, 3.0, 0.1)

if st.button("Qual será sua Iris?"):
    parametros = pd.DataFrame(
        [[Comprimento_Sepala, Largura_Sepala, Comprimento_Petala, Largura_Petala]],
        columns=["Comprimento_Sepala", "Largura_Sepala", "Comprimento_Petala", "Largura_Petala"] )

# Parte da previsão final e mostrar resultado

    previsao = PImodelo.predict(parametros)
    iris_esperada = florzinha.inverse_transform(previsao)[0]
    st.success(f"Olha só, parece que com seus parâmetros, a sua Iris provavelmente seria uma **{iris_esperada}** !")

# Segunda parte: Integração do Wokwi e sua análise de dados -----------------------------------------------------------


# Criando o título, e conectando o token do wokwi e id do projeto.
def wokwi_analise ():
    st.subheader("Dashboard do Wokwi com IoT e Análise de Dados")

    # Por motivos de teste, e como isso é apenas um projeto, a chave vai ficar aqui no código
    # Sendo usada ou não dependendo do contexto para testes
    # Mas no streamlit de fato esta rodando pelo secrets

    #token = st.secrets["Wokwi_Token"] #Chave está no Secrets do Streamlit para funcionar melhor
    token = "wok_MoozVa8jD1OnxgB1A0PxNDj45cpWncCo20baeb57" 
    client = WokwiClientSync(token=token)
    client.connect()

    json_path = "diagram.json"
    PROJECT_ID = client.upload_file(json_path)
    st.info(f"ID temporário: {PROJECT_ID}")

    # PROJECT_ID = 446990024295294977 Guardando pra mais tarde o ID se precisar, está aqui apenas para referência

    simulacao = client.start_simulation(PROJECT_ID)
    time.sleep(3)

# Recebimento de Dados do Wokwi

    grafico1 = st.empty()
    tabela1 = st.empty()
    st.info("Recebendo dados da simulação")

    dadoWokwi = {"voltage": [], "current": [], "power": [], "energy": []}

    for nao_usada in range(100):
        linha = simulacao.readline()
        if linha:
            try:
                partes = linha.decode().strip().split(",")
                if len(partes) == 4:
                    v, c, p, e = partes
                    dadoWokwi["voltage"].append(float(v))
                    dadoWokwi["current"].append(float(c))
                    dadoWokwi["power"].append(float(p))
                    dadoWokwi["energy"].append(float(e))
            except Exception as e:
                st.warning(f"Oops, algo deu errado no processamento: {e}") #Ver isso aqui depois
                continue


# Gráficos e Tabelas

        df = pd.DataFrame(dadoWokwi)
        grafico1.line_chart(df[["voltage","current"]])
        tabela1.dataframe(df)
        time.sleep(1)

    simulacao.stop_simulation()
    st.success("Fim da simulação")

wokwi_analise()