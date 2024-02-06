import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from streamlit_dynamic_filters import DynamicFilters
from scipy.stats import zscore



st.set_page_config(page_title="NABERS Dashboard",
                  layout="wide")
st.title('Overview on NABERS data KPIs')


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

# data_loading = st.text('loading data...')
# data_loading.text('loading data...(using st.cache_data)!')
dynamic_filters = DynamicFilters(data, filters=['state', 'premisetype', 'ratingtype'])
st.sidebar.header("Filter by review type:")
with st.sidebar:
    dynamic_filters.display_filters()

filtered_data = dynamic_filters.filter_df()
col_1, col_2= st.columns(2)

energy_filter = ['energy', 'electricity', 'aaa', 'gas', 'diesel', 'rei', 'kwh']
environment_filter = ['ieq', 'thermal', 'air', 'acoustic', 'lighting', 'office', 'apartment', 'bed', 'rooms', 'shopping']
waste_filter = ['waste']
water_filter = ['water']
col_list = list(filtered_data.columns)
energy_cols = [i for i in col_list if any(keyword in i for keyword in energy_filter)]
environment_cols = [i for i in col_list if any(keyword in i for keyword in environment_filter)]
waste_cols = [i for i in col_list if any(keyword in i for keyword in waste_filter)]
water_cols = [i for i in col_list if any(keyword in i for keyword in water_filter)]
filtered_cols = energy_cols + environment_cols + waste_cols + water_cols

with col_1:
    st.subheader('Map of report locations ')

    # Consider making a color based on the type!
    
    z = filtered_data[['latitude', 'longitude', 'ratingtype','color']]
    
    z = z.dropna(axis=0).reset_index()
    st.map(data=z, latitude='latitude', longitude='longitude', color='color', size=.5,zoom=3)

    unique_colors = z['color'].unique()

    # Display the unique colors

    # Create a DataFrame from the color_code dictionary
    color_code = {'Waste': '#FFA500', 'Indoor Environment': '#355E3B', 'Energy': '#FFFF00', 'Water': '#0000FF'}
    df_color_legend = pd.DataFrame(list(color_code.items()), columns=['Category', 'Color Code'])

    # Define the function to apply background colors
    def color_cells(val):
        return f'background-color: {val};'

    # Apply the style to the entire DataFrame
    styled_df_color_legend = df_color_legend.style.applymap(color_cells, subset=['Color Code'])

    # Display the styled DataFrame in Streamlit
    st.write('Color Legend', styled_df_color_legend)

with col_2:
    z4 = filtered_data[['premisetype', 'state']]
    st.subheader('state and premisetype bar chart')
    st.plotly_chart(px.bar(z4, x='state', color='premisetype', barmode='stack', hover_data=['premisetype']))


    category_dict = {'energy': energy_cols, 'social': environment_cols, 'waste': waste_cols, 'water': water_cols}
    colors = ['#FF0000','#008000']
    st.subheader('Stacked Bar Chart of Carbonneutral Count by Rating Type')
    grouped_data = filtered_data.groupby(['ratingtype', 'carbonneutral']).size().reset_index(name='count')
    fig = px.bar(grouped_data, x='ratingtype', y='count', color='carbonneutral', color_discrete_sequence=colors,
            )

    st.plotly_chart(fig)

outliers_list = []

for column in data.columns:
    if data[column].dtype in ['int64', 'float64']:
        col_vals = data[column].dropna()
        z_scores = zscore(col_vals)
        threshold = 2

        if not col_vals.empty: 
            outlier_indices = col_vals.index[abs(z_scores) > threshold]
            outliers_df = data.iloc[outlier_indices].dropna(axis=1,how='all')
            percent_outliers = (len(outliers_df) / len(col_vals)) * 100
        else:
            outliers_df = pd.DataFrame() 
            percent_outliers = 0 

        outliers_list.append({'column': column, 'percent_outliers': percent_outliers, 'outliers_data': outliers_df})

outliers_df = pd.DataFrame(outliers_list)

selected_column = st.selectbox('Select column to see outliers table', outliers_df['column'])


filtered_outliers_df = outliers_df[outliers_df['column'] == selected_column]


if not filtered_outliers_df.empty and filtered_outliers_df['percent_outliers'].values[0] != 0:

    st.write(filtered_outliers_df.drop(columns='outliers_data'))

    st.dataframe(filtered_outliers_df['outliers_data'].values[0].dropna(how='all').drop(columns=['_merge', 'color']))
else:
    st.warning(f"No data or percent_outliers is 0 for the selected column: {selected_column}")