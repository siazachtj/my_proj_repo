import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from streamlit_dynamic_filters import DynamicFilters



st.set_page_config(page_title="NABERS Dashboard",
                  layout="wide")
st.title('Water related KPIs')


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
dynamic_filters = DynamicFilters(data, filters=['state', 'premisetype'])
st.sidebar.header("Filter by review type:")
with st.sidebar:
    dynamic_filters.display_filters()

filtered_data = dynamic_filters.filter_df()
col_1, col_2= st.columns(2)

st.subheader('Scatter/Histogram plot of Water Star Rating Value over certification validation date')
result = filtered_data.groupby('certificatevalidto')['waterstarratingvalue'].mean().reset_index()
fig = px.scatter(result, x='certificatevalidto',y='waterstarratingvalue',marginal_x="histogram", marginal_y="rug")
fig.update_layout(
    xaxis_title='Carbon Neutral Expiry Date',
    yaxis_title='Rating Value',
    height=600,  # Set the height (in pixels) as needed
    width=1500    # Set the width (in pixels) as needed
)
st.plotly_chart(fig)
with col_1:
    mean_value = filtered_data['waterstarratingvalue'].mean()

    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=mean_value,
        title={'text': 'Water Star Rating'},
        gauge={'axis': {'range': [0, 6]},
               'bar': {'color': 'blue'},
               'steps': [
                   {'range': [0, 3], 'color': 'red'},
                   {'range': [3, 4.5], 'color': 'yellow'},
                   {'range': [4.5, 6], 'color': 'green'}]}))
    
    st.plotly_chart(fig)
    st.subheader('Water consumption vs waterconsumption without RW')
    water_consum = filtered_data[['waterconsumption','waterconsumptionworw']]
    fig = px.violin(water_consum)
    st.plotly_chart(fig)

    
with col_2:
    mean_value = filtered_data['waterstarratingvaluenorw'].mean()
    fig = go.Figure(go.Indicator(
        mode='gauge+number',
        value=mean_value,
        title={'text': 'Water Star Rating without RW'},
        gauge={'axis': {'range': [0, 6]},
               'bar': {'color': 'blue'},
               'steps': [
                   {'range': [0, 3], 'color': 'red'},
                   {'range': [3, 4.5], 'color': 'yellow'},
                   {'range': [4.5, 6], 'color': 'green'}]}))
    st.plotly_chart(fig)
    st.subheader('Water Intensity vs Water Intensity without RW')
    water_intensity = filtered_data[['waterintensity','waterintensitynorw']] 
    fig = px.violin(water_intensity)
    st.plotly_chart(fig)    
# #fix this
    # # can consider making a color based on the type! 
    # # use folium?
    # # use PremisesName as a marker
    # z= data[['Latitude','Longitude','RatingType']]
    # color_code = {'Waste':'#FFA500', 'Indoor Environment' : '#008000', 'Energy' : '#FFFF00', 'Water':'#0000FF'}
    # z['color'] = z['RatingType'].map(color_code)
    # # z['color']
    # z = z.dropna()
    # st.map(data=z,latitude='Latitude',longitude='Longitude',color='color',zoom=3)
    # st.subheader('violin chart!')
    # z2 = data.groupby('PremiseID').size()
    # violin = px.violin(z2, y=z2.values)
    # st.plotly_chart(violin)


    # st.subheader('Premisetype barchart!')
    # z3 = data['PremiseType']
    # st.plotly_chart(px.bar(z3))
    # z4 = data[['PremiseType','State']]
    # st.subheader('stacked barchart, state and premisetype!')
    # st.plotly_chart(px.bar(z4,x='State',color='PremiseType',barmode='stack',hover_data=['PremiseType']))
    # col_list = [cols.lower() for cols in data.columns]

    # energy_filter = ['energy','electricity', 'aaa','gas','diesel','rei','kwh']
    # environment_filter = ['ieq','thermal','air','acoustic','lighting','office','apartment','bed','rooms','shopping']
    # waste_filter = ['waste','recycle']
    # water_filter = ['water']

    # energy_cols = [i for i in col_list if any(keyword in i for keyword in energy_filter)]
    # environment_cols = [i for i in col_list if any(keyword in i for keyword in environment_filter)]
    # waste_cols = [i for i in col_list if any(keyword in i for keyword in waste_filter)]
    # water_cols = [i for i in col_list if any(keyword in i for keyword in water_filter)]

