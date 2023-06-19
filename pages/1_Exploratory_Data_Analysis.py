#=========================================================#
#------------------ Import Libraries -------------------- #
#=========================================================#

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from PIL import Image


#=========================================================#
#-------------------- Functions ------------------------- #
#=========================================================#

def preprocess_data(df):

    """ 
    This functions has the responsability to cleaning and preprocessing the dataframe
    Input:  dataframe
    Output: dataframe

    """

    # Preprocessing feature 'age'
    df['age'] = df['age'].apply(lambda x: x/365)
    df['age'] = df['age'].astype(int)

    # Drop the ID column
    df = df.drop('id', axis=1)

    # Removing outliers using IQR approach
    def remove_outlier(col):
        Q1 = np.percentile(df[col], 25, interpolation='midpoint')
        Q3 = np.percentile(df[col], 75, interpolation='midpoint')
        IQR = Q3 - Q1

        upper = np.where(df[col] >= (Q3 + 1.5 * IQR))
        lower = np.where(df[col] <= (Q1 - 1.5 * IQR))

        # Remove outliers
        df.drop(upper[0], inplace=True)
        df.drop(lower[0], inplace=True)

    remove_outlier('height')

    # Feature Engineering
    df['BMI'] = df['weight'] / ((df['height'] / 100) ** 2)

    return df

#=========================================================#
#------------- Logical Structure of the code ------------ #
#=========================================================#

# ----- Data import and processing ------ #

# Load the data
df= pd.read_csv('dataset/cardio_disease_dataset.csv', delimiter = ';', nrows = None)  # Replace 'your_dataset.csv' with your actual dataset filename

# Preprocess the data
df = preprocess_data(df)

#=========================================================#
#----------------- Streamlit Layout --------------------- #
#=========================================================#

# Page configuration
st.set_page_config(
    page_title = 'Exploratory Data Analysis',
    page_icon = '📈',
    layout='wide'
)

# Sidebar
image = Image.open ('images/cardio_image.png')

st.sidebar.markdown ("## Please select the checkboxes listed to explore the data:")
st.sidebar.image (image, width=100)
st.sidebar.markdown ("""---""")
#st.sidebar.markdown ("## Please select the checkboxes listed to explore the data:")
show_data = st.sidebar.checkbox ("Take a look at the Dataframe")
show_statistics = st.sidebar.checkbox ("Take a look at the Summary Statistics")
show_graph1 = st.sidebar.checkbox("Distribution of the Target Variable")
show_graph2 = st.sidebar.checkbox("Age frequency on the dataframe")
show_graph3= st.sidebar.checkbox("Relationshipg between Age and Cardiovascular disease")
show_graph4= st.sidebar.checkbox("Gender and the presence of Cardiovascular disease")
show_graph5= st.sidebar.checkbox("Cholesterol and Glucose levels")
#show_graph6= st.sidebar.checkbox("Correlation matrix between all features")

#=========================================================#
#------------- Exploratory Data Analysis ---------------- #
#=========================================================#

# ----- Resume and header ------ #

# Page Title
st.title("Exploratory Data Analysis")
image = Image.open ('images/cardio_binary.jpg')
# Insert image
st.image(image, width=550)

# Project Description
st.markdown("""
The dataset presents 70,000 data separated into 12 distinct characteristics, such as age, gender, blood pressure, cholesterol, smoker or non-smoker, etc.

The target class will be **'cardio'**, which will be described as: **'0' when the patient is healthy and '1' when the patient has cardiovascular disease.**
""")

# Display the data description
st.subheader("Data Description")
st.markdown("""
1. **Age**: Objective Feature | age | int (days)
2. **Height**: Objective Feature | height | int (cm)
3. **Weight**: Objective Feature | weight | float (kg)
4. **Gender**: Objective Feature | gender | categorical code | 1: woman, 2: man
5. **Systolic blood pressure**: Examination Feature | ap_hi | int
6. **Diastolic blood pressure**: Examination Feature | ap_lo | int
7. **Cholesterol**: Examination Feature | cholesterol | 1: normal, 2: above normal, 3: well above normal
8. **Glucose**: Examination Feature | gluc | 1: normal, 2: above normal, 3: well above normal
9. **Smoking**: Subjective Feature | smoke | binary
10. **Alcohol intake**: Subjective Feature | alco | binary
11. **Physical activity**: Subjective Feature | active | binary
12. **Presence or absence of cardiovascular disease**: Target Variable | cardio | 1: disease, 0: no
""")

# ----- EDA ------ #
# ----- Checkboxs ------ #

# Display the processed data and its summary statistics side by side
col1, col2 = st.columns(2)

# Check if the checkbox is selected
if show_data:
    # Display processed data in the first column
    col1.subheader("Processed Data")
    col1.write(df.head(8))

if show_statistics:
    # Display summary statistics in the second column
    col2.subheader("Summary Statistics")
    col2.write(df.describe())

####################################
# ----- Target Distribution ------ #
####################################

# Check if the checkbox is selected
if show_graph1:
    # Target Distribution
    col1.subheader("Target Distribution")
    col1.markdown("**Checking the distribution of the variable 'cardio' in the dataset:**")

    plt.figure(figsize=(12, 8))
    fig = sns.countplot(x='cardio', data=df, palette='colorblind', edgecolor='black')
    fig.set_title('Distribution of the target variable', fontsize=18, weight='bold')

    # Display the plot
    col1.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Display the percentage
    col1.write("Patients with heart disease represent **49.3% of the dataset**")

############################
# ----- Feature Age ------ #
############################

# Histogram of age frequency

if show_graph2:

    col2.subheader("Histogram of Age frequency on the dataset")

    plt.figure(figsize=(12,8))
    fig = sns.histplot(data=df, x = 'age', bins = 30, edgecolor ='black');
    fig.set_title('Histogram of Age frequency on the dataset', fontsize = 18, weight = 'bold')

    # Display the plot
    col2.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # mean age
    col2.write("The average age in the DataFrame is **53 years.**")

# Relationshipg between AGE and Target Cardio

if show_graph3:

    st.subheader("Relationship of increasing Age with the presence of Cardiovascular disease")
    # Filter the DataFrame to get only people with cardio = 0
    df_cardio_0 = df[df['cardio'] == 0]

    # Filter the DataFrame to get only people with cardio = 1
    df_cardio_1 = df[df['cardio'] == 1]

    # Count per age
    count_cardio_0 = df_cardio_0['age'].value_counts().sort_index()
    count_cardio_1 = df_cardio_1['age'].value_counts().sort_index()

    # Combine the two groups
    combined_index = count_cardio_0.index.union(count_cardio_1.index)

    # Reindexing
    count_cardio_0 = count_cardio_0.reindex(combined_index, fill_value=0)
    count_cardio_1 = count_cardio_1.reindex(combined_index, fill_value=0)

    # Fig size
    plt.figure(figsize=(16, 6))

    # Combined graph
    plt.bar(combined_index, count_cardio_0, label='Without Cardio disease', color='darkblue')
    plt.bar(combined_index, count_cardio_1, bottom=count_cardio_0, label='With Cardio disease', color='darkorange')

    # Layout
    plt.title('Relationship of increasing Age with the presence of Cardiovascular disease', fontweight='bold')

    plt.xlabel('Age', fontweight='bold')
    plt.ylabel('Count', fontweight='bold')

    plt.grid(False)
    plt.gca().set_facecolor('white')

    plt.legend()

    # show
    plt.show()
    st.pyplot(plt.gcf())

    # Conclusion
    st.write("The representation demonstrates a **turnaround that occurs after the age of 53**, when the number of patients **with heart disease exceeds the number of patients without heart disease** in the sample.")

############################
# ----- Feature Gender ------ #
############################

if show_graph4:

    col1.subheader("Gender and the presence of Cardiovascular disease")
    plt.figure(figsize=(10, 6))
    sns.set(font_scale=1)

    ax = sns.countplot(x='gender', hue='cardio', data=df,
                    palette='deep',
                    edgecolor='black')

    # Substituir os rótulos '1' e '2' por 'Man' e 'Woman'
    ax.set_xticklabels(['Man', 'Woman'])

    # Definir a legenda personalizada
    legend_labels = ['Without Cardio disease', 'With Cardio disease']
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles, legend_labels)

    # Adicionar a contagem acima das barras
    for i in ax.patches:
        ax.annotate(i.get_height(),
                    (i.get_x() + i.get_width() / 2, i.get_height()),
                    ha='center', va='baseline', fontsize=12, color='black',
                    xytext=(0, 3),
                    textcoords='offset points')

    # show
    plt.show()
    col1.pyplot(plt.gcf())

    # Conclusion
    col1.write("Apparently there is **no strong correlation between gender and the presence of Cardiovascular disease.**")

############################
# - Categorical Features - #
############################

if show_graph5:

    #Cholesterol Levels
    col1, col2 = st.columns(2)

    # Relationship between cholesterol levels and cardio
    with col1:
        st.subheader("Relationship between cholesterol levels and cardio")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlabel('Cardio', fontsize=12)
        ax.set_ylabel('Cholesterol', fontsize=12)
        ax.set_title('Cholesterol Levels x Cardio', fontsize=18, color='black')

        cholesterol_labels = {1: 'Normal', 2: 'Above normal', 3: 'Well above normal'}

        df.groupby('cholesterol')['cardio'].mean().rename(cholesterol_labels).plot.barh(color='darkred', edgecolor='black')

        st.pyplot(fig)

        # Conclusion
        st.write("There is a direct relationship in that the **higher the Cholesterol levels, the greater the presence of cardiovascular diseases.**")

    # Relationship between glucose levels and cardio
    with col2:
        st.subheader("Relationship between glucose levels and cardio")

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.set_xlabel('Cardio', fontsize=12)
        ax.set_ylabel('Gluc', fontsize=12)
        ax.set_title('Glucose Levels x Cardio', fontsize=18, color='black')

        gluc_labels = {1: 'Normal', 2: 'Above normal', 3: 'Well above normal'}

        df.groupby('gluc')['cardio'].mean().rename(gluc_labels).plot.barh(color='purple', edgecolor='black');

        st.pyplot(fig)

        # Conclusion
        st.write("There is also a direct relationship in that the **higher the Glucose levels, the greater the presence of cardiovascular diseases.**")

########################################
# - Correlation between all features - #
########################################

#if show_graph6:

    #st.subheader("Correlation matrix between all features")
    #plt.figure(figsize=(10, 8))
    #sns.heatmap(df.corr(), annot=True, fmt='.0%', cmap='YlGnBu')
    #plt.title('Correlation between features', fontsize = 14);

    #st.pyplot(plt.gcf())
