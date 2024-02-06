import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from streamlit_dynamic_filters import DynamicFilters
from PIL import Image


st.set_page_config(page_title="NABERS Dashboard",
                  layout="wide")
image = Image.open('NABERS_logo.jpg')
image = image.resize((1000, 800))
st.title('Welcome to the NABERS data dashboard!')
st.image(image)





@st.cache_data

def create_dynamic_pie_chart(category_dict):
    count_dict = {category: len(columns) for category, columns in category_dict.items()}
    return px.pie(names=list(count_dict.keys()), values=list(count_dict.values()), title='KPI count per report category')

def load_data():
    data = pd.read_csv('NABERS.csv', index_col=None)

    # data[['Latitude','Longitude']] = data[['Latitude','Longitude']]
    # data[['Latitude','Longitude']]= data[['Latitude','Longitude']].astype(str)
    # data.rename(columns={'Latitude':'latitude', 'Longitude':'longitude'},inplace=True)
    color_code = {'Waste': '#FFA500', 'Indoor Environment': '#355E3B', 'Energy': '#FFFF00', 'Water': '#0000FF'}
    data['color'] = data['ratingtype'].map(color_code)
    return data

# data_loading = st.text('loading data...')
data = load_data()
# data_loading.text('loading data...(using st.cache_data)!')
dynamic_filters = DynamicFilters(data, filters=['state', 'premisetype', 'ratingtype'])
filtered_data = data


dynamic_filters = DynamicFilters(data, filters=['state', 'premisetype', 'ratingtype'])
filtered_data = data

st.markdown(
    """

    ### Who are NABERS?
    Since 1998, NABERS (National Australian Built Environment Rating System) provides simple, reliable, and comparable sustainability measurement you can trust across building sectors like hotels, shopping centres, apartments, offices, data centres, and more.
    
    ### What is the source for this dashboard?
    The NABERS rating dataset used for this analysis was provided from [NABERS rating page](https://www.nabers.gov.au/ratings/find-a-current-rating)
    
    ### What is the purpose of this dashboard?

    - Provide [high-level](/overview) information regarding on KPIs, premise types and distribution of carbon neutrality across all categories.
    - Breakdown distributions and visualise aggregates for the 4 main rating categories.

        - [Energy](energy) 

        - [Water](water)

        - [Waste](waste)

        - [Indoor Environment](indoor_env)
    
"""
)
energy_filter = ['energy','electricity', 'aaa','gas','diesel','rei','kwh']
environment_filter = ['ieq','thermal','air','acoustic','lighting','office','apartment','bed','rooms','shopping']
waste_filter = ['waste','recyclerate']
water_filter = ['water']
col_list = list(filtered_data.columns)
energy_cols = [i for i in col_list if any(keyword in i for keyword in energy_filter)]
environment_cols = [i for i in col_list if any(keyword in i for keyword in environment_filter)]
waste_cols = [i for i in col_list if any(keyword in i for keyword in waste_filter)]
water_cols = [i for i in col_list if any(keyword in i for keyword in water_filter)]


category_dict = {
    'Energy': energy_cols,
    'Environment': environment_cols,
    'Waste': waste_cols,
    'Water': water_cols
}
st.plotly_chart(create_dynamic_pie_chart(category_dict))