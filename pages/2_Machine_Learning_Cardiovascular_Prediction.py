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
        return None
    bmi = weight / ((height / 100) ** 2)
    return bmi

# Carregar o modelo
model = load_model()

# Interface do usuário usando Streamlit
def main():

    st.set_page_config(
    page_title = 'Machine Learning',
    page_icon="🧠",
    layout='wide'
)
    # Título do aplicativo
    st.image("https://agm.org.br/wp-content/uploads/2017/10/03102017_divulgacao_doenca_cardiaca.jpg", width=200)
    st.title("Aplicativo de Previsão Cardiovascular")

    # Formulário para entrada de dados
    st.header("Enter the patient's data in the following fields:")
    age = st.slider("Age (in years)", 1, 100)
    gender_options = {"Male": 1, "Female": 2}
    gender = st.selectbox("Gender", list(gender_options.keys()))
    height = st.number_input("Height (in cm)", format="%f")
    weight = st.number_input("Weight (in kg)", format="%f")
    ap_hi = st.number_input("Systolic Blood Pressure (ap_hi) in mmHg", format="%f")
    ap_lo = st.number_input("Diastolic Blood Pressure (ap_lo) in mmHg", format="%f")
    cholesterol_options = {"Normal": 1, "Above Normal": 2, " Well Above Normal": 3}
    cholesterol = st.selectbox("Cholesterol", list(cholesterol_options.keys()))
    gluc_options = {"Normal": 1, "Above Normal": 2, " Well Above Normal": 3}
    gluc = st.selectbox("Glucose", list(gluc_options.keys()))
    smoke_options = {"No": 0, "Yes": 1}
    smoke = st.selectbox("Regular smoker", list(smoke_options.keys()))
    alco_options = {"No": 0, "Yes": 1}
    alco = st.selectbox("Regular consumption of alcohol", list(alco_options.keys()))
    active_options = {"No": 0, "Yes": 1}
    active = st.selectbox("Regular physical activity", list(active_options.keys()))

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
    if st.button("Evaluate the patient's risk of cardiovascular disease"):
        # Prever a classe
        prediction = predict(model, input_data)

        # Exibir resultado da previsão
        st.header("Prediction Result")
        if prediction[0] == 0:
            st.write("**Low** Cardiovascular Risks")
        else:
            st.write("**High** Cardiovascular Risks")

if __name__ == "__main__":
    main()


