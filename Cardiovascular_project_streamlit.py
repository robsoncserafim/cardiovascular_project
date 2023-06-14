import streamlit as st
import pickle
import pandas as pd
import numpy as np
import sklearn
from sklearn.ensemble import GradientBoostingClassifier

# Função para carregar o modelo
def load_model():
    with open('gbm_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Função para realizar a previsão
def predict(model, input_data):
    prediction = model.predict(input_data)
    return prediction

# Função para calcular o BMI
def calculate_bmi(height, weight):
    if height == 0:
        st.error("Altura inválida. Certifique-se de inserir a altura em centímetros.")
        return None
    bmi = weight / ((height / 100) ** 2)
    return bmi

# Carregar o modelo
model = load_model()

# Interface do usuário usando Streamlit
def main():

    st.set_page_config(layout="wide")
    # Título do aplicativo
    st.image("https://agm.org.br/wp-content/uploads/2017/10/03102017_divulgacao_doenca_cardiaca.jpg", width=400)
    st.title("Aplicativo de Previsão Cardiovascular")


    # Formulário para entrada de dados
    st.header("Insira os valores das colunas:")
    age = st.slider("Idade (em anos)", 1, 100)
    gender_options = {"Masculino": 1, "Feminino": 2}
    gender = st.selectbox("Gênero", list(gender_options.keys()))
    height = st.number_input("Altura (em cm)", format="%f")
    weight = st.number_input("Peso (em kg)", format="%f")
    ap_hi = st.number_input("Pressão Sistólica (ap_hi) em mmHg", format="%f")
    ap_lo = st.number_input("Pressão Diastólica (ap_lo) em mmHg", format="%f")
    cholesterol_options = {"Normal": 1, "Acima do Normal": 2, "Muito Acima do Normal": 3}
    cholesterol = st.selectbox("Colesterol", list(cholesterol_options.keys()))
    gluc_options = {"Normal": 1, "Acima do Normal": 2, "Muito Acima do Normal": 3}
    gluc = st.selectbox("Glicose", list(gluc_options.keys()))
    smoke_options = {"Não": 0, "Sim": 1}
    smoke = st.selectbox("Fumante", list(smoke_options.keys()))
    alco_options = {"Não": 0, "Sim": 1}
    alco = st.selectbox("Consumo de Álcool", list(alco_options.keys()))
    active_options = {"Não": 0, "Sim": 1}
    active = st.selectbox("Atividade Física", list(active_options.keys()))

    # Calcular o BMI
    bmi = calculate_bmi(height, weight)
    if bmi is None:
        return

    # Converter os valores em uma estrutura de dados utilizada pelo modelo
    input_data = pd.DataFrame({
        'age': [age],
        'gender': [gender_options[gender]],
        'height': [height],
        'weight': [weight],
        'ap_hi': [ap_hi],
        'ap_lo': [ap_lo],
        'cholesterol': [cholesterol_options[cholesterol]],
        'gluc': [gluc_options[gluc]],
        'smoke': [smoke_options[smoke]],
        'alco': [alco_options[alco]],
        'active': [active_options[active]],
        'BMI': [bmi]
    })

    # Botão para avaliar o risco do paciente ter doença cardiovascular
    if st.button("Avaliar risco do paciente ter doença cardiovascular"):
        # Prever a classe
        prediction = predict(model, input_data)

        # Exibir resultado da previsão
        st.header("Resultado da Previsão")
        if prediction[0] == 0:
            st.write("Risco Cardiovascular Baixo")
        else:
            st.write("Risco Cardiovascular Alto")

if __name__ == "__main__":
    main()

