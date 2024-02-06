import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="NABERS Dashboard",
                  layout="wide")
st.title('NABERS data dashboard!')

@st.cache_data


def load_data(nrows):
    data = pd.read_csv('downloaded_file_date_11-17-2023_time_21-37.csv',index_col=False,nrows=nrows)
    # data[['Latitude','Longitude']] = data[['Latitude','Longitude']]
    # data[['Latitude','Longitude']]= data[['Latitude','Longitude']].astype(str)
    # data.rename(columns={'Latitude':'latitude', 'Longitude':'longitude'},inplace=True)

    return data

# data_loading = st.text('loading data...')
data = load_data(3000)
# data_loading.text('loading data...(using st.cache_data)!')

st.sidebar.header("Filter by review type:")
ratings = st.sidebar.multiselect(
    "Select one or more review types:",
    options=data['RatingType'].unique()
)

premise_types = st.sidebar.multiselect(
    "Select one or more premise types:",
    options=data['PremiseType'].unique()
)

areas = st.sidebar.multiselect(
    "Select one or more areas:",
    options=data['State'].unique()
)

# df_selection = data.query(
#     "RatingType == @ratings" 
#     "PremiseType == @premise_types"
#     "State == @areas" 
#     )

col_1, col_2= st.columns(2)

with col_1:
    st.subheader('maps!')

    #fix this
    # can consider making a color based on the type! 
    # use folium?
    # use PremisesName as a marker
    z= data[['Latitude','Longitude','RatingType']]
    color_code = {'Waste':'#FFA500', 'Indoor Environment' : '#008000', 'Energy' : '#FFFF00', 'Water':'#0000FF'}
    z['color'] = z['RatingType'].map(color_code)
    # z['color']
    z = z.dropna()
    st.map(data=z,latitude='Latitude',longitude='Longitude',color='color',zoom=3)
    st.subheader('violin chart!')
    z2 = data.groupby('PremiseID').size()
    violin = px.violin(z2, y=z2.values)
    st.plotly_chart(violin)

with col_2:
    # st.subheader('Premisetype barchart!')
    # z3 = data['PremiseType']
    # st.plotly_chart(px.bar(z3))
    z4 = data[['PremiseType','State']]
    st.subheader('stacked barchart, state and premisetype!')
    st.plotly_chart(px.bar(z4,x='State',color='PremiseType',barmode='stack',hover_data=['PremiseType']))
    col_list = [cols.lower() for cols in data.columns]

    energy_filter = ['energy','electricity', 'aaa','gas','diesel','rei','kwh']
    environment_filter = ['ieq','thermal','air','acoustic','lighting','office','apartment','bed','rooms','shopping']
    waste_filter = ['waste','recycle']
    water_filter = ['water']

    energy_cols = [i for i in col_list if any(keyword in i for keyword in energy_filter)]
    environment_cols = [i for i in col_list if any(keyword in i for keyword in environment_filter)]
    waste_cols = [i for i in col_list if any(keyword in i for keyword in waste_filter)]
    water_cols = [i for i in col_list if any(keyword in i for keyword in water_filter)]

    dict_test = {'energy':len(energy_cols), 'social': len(environment_cols), 'waste':len(waste_cols), 'water': len(water_cols)}

    st.subheader('KPI count per report category!')
    st.plotly_chart(px.pie(names=list(dict_test.keys()),values= list(dict_test.values())),title='KPI count per report category')