import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("learning.csv")

PImodelo= LinearRegression()
x = df[["toneladas"]]
y = df[["preco"]]

PImodelo.fit(x,y)

st.title("Prever o valor da tonelada de material desconhecido")
st.divider()

toneladas = st.number_input("Digite o peso em toneladas: ")

if toneladas:
    preco_esperado = PImodelo.predict([[toneladas]])[0][0]
    st.write(f"O preco de {toneladas:.2f} de material é de R${preco_esperado:.3f} .")