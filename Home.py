import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Home',
    page_icon="👋",
    layout='wide'
)

st.write("#### Welcome to my Streamlit Project! 👋")

image = Image.open ('images/cardio_image.png')
st.sidebar.image (image, width=250)

st.sidebar.markdown ('# Cardiovascular Disease - Data Science Project')

st.sidebar.markdown ('#### by Robson Serafim')
cols1, cols2, cols3 = st.sidebar.columns(3)

cols1.markdown("[![Title](https://img.icons8.com/?size=1x&id=13930&format=png)](https://www.linkedin.com/in/robson-castro-serafim/)")
cols2.markdown("[![Title](https://img.icons8.com/material-outlined/48/000000/github.png)](https://www.gitshowcase.com/robsoncserafim)")
cols3.markdown("[![Title](https://img.icons8.com/?size=1x&id=XVNvUWCvvlD9&format=png)](https://medium.com/@robson.serafim)")

# Page Title
st.title("Cardiovascular Disease Project")
image = Image.open ('images/cardio_image_EDA.jpg')
# Insert image
st.image(image, width=800)

st.markdown (
"""

I strongly believe that the primary objective of data science is to make a meaningful contribution to society by providing valuable insights. 

The healthcare industry is one area where the application of data science holds immense significance and offers numerous benefits to society.

The web application provides an easy-to-navigate interface where you can explore different aspects of the project. 
### So, how to navigate in this app?

**- Exploratory Data Analysis:**

    - The Exploratory Data Analysis section presents statitical insights and visualizations using popular libraries such as Seaborn, Plotly, and Matplotlib. These visualizations help us to understanding the data and gaining insights from it.

**- Machine Learning:**

    - Classification Machine Learning Model that utilizes Gradient Boosting to predict the presence or absence of a Cardiovascular disease. This model leverages the power of data to make accurate predictions and assist in healthcare decision-making.


#### Feel free to explore and interact with the application! 
#### It provides an opportunity to gain insights and experience the predictive capabilities of the deployed Machine Learning Model.

     
""")





