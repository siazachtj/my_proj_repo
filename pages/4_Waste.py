import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from streamlit_dynamic_filters import DynamicFilters
import plotly.figure_factory as ff



st.set_page_config(page_title="NABERS Dashboard",
                  layout="wide")
st.title('Waste related KPIs')


@st.cache_data


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

st.subheader('Scatter/Histogram plot of Waste Star Rating Value over certification validation date')
result = filtered_data.groupby('certificatevalidto')['wastestarratingvalue'].mean().reset_index()
fig = px.scatter(result, x='certificatevalidto',y='wastestarratingvalue',marginal_x="histogram", marginal_y="rug")
fig.update_layout(
    xaxis_title='Carbon Neutral Expiry Date',
    yaxis_title='Rating Value',
    height=600,  # Set the height (in pixels) as needed
    width=1500    # Set the width (in pixels) as needed
)
st.plotly_chart(fig)

with col_1:
    st.subheader('Gauge chart of Waste star rating value')
        
    mean_value = data['wastestarratingvalue'].mean()

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
    fig.update_layout(width=500, height=400)
    st.plotly_chart(fig)
with col_2:
    st.subheader('Distribution plot of reycle rate')
    fig = ff.create_distplot([data['recyclerate'].dropna()], ['recyclerate'], show_hist=True, histnorm='probability density')
    st.plotly_chart(fig)

