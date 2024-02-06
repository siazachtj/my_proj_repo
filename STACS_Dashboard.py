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

def not_all_upper(st):
    if isinstance(st,str):
        return " ".join([word.title() if not word.isupper() else word for word in st.split()])
    else:
        pass

def checker(words):
    if isinstance(words,str):
        return all(word.isupper() for word in words.split())
    else:
        return False



def clean_df(new_file):
    new_file.columns = [col.lower() for col in new_file.columns]
    objects = new_file.dtypes.loc[lambda x: x == 'object']
    objects_list = list(objects.index)
    for i in objects.index.to_list():
        new_file[i] = new_file[i].apply(lambda x: ' '.join(x.split()) if isinstance(x,str) else x)
        new_file[i] = new_file[i].apply(lambda x: x.strip() if isinstance(x,str) else x)

    for col in new_file[objects_list]:
        print(col)
        col_ratio = new_file[col].apply(checker).sum()/ new_file[col].apply(lambda x: isinstance(x, str)).sum()
        print(col_ratio)
        if col_ratio > 0.5:
            new_file[col] = new_file[col].apply(lambda x: x.upper() if isinstance(x,str) else x)
        else:
            new_file[col] = new_file[col].apply(not_all_upper)
            
    new_file[['certificatevalidto','carbonneutralexpirydate']] = new_file[['certificatevalidto','carbonneutralexpirydate']].apply(pd.to_datetime)
    new_file['combined_column'] = new_file['premiseid'] + '_' + new_file['ratingreferencenumber'].astype(str) + '_' + new_file['ratingtype'] + '_' + new_file['certificatevalidto'].astype(str)
    return new_file

df = pd.read_csv("downloaded_file_date_11-17-2023_time_21-37.csv",index_col=False)
data = clean_df(df)

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