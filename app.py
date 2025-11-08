# Lista das coisas que estão sendo importadas

import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

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

st.title("Prever qual a espécie de Iris estamos vendo")
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