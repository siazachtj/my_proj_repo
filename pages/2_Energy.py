import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from sqlalchemy import create_engine
from streamlit_dynamic_filters import DynamicFilters



st.set_page_config(page_title="NABERS Dashboard",
                  layout="wide")
st.title('Energy related KPIs')

@st.cache_data



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

def load_data(data):
    color_code = {'Waste': '#FFA500', 'Indoor Environment': '#355E3B', 'Energy': '#FFFF00', 'Water': '#0000FF'}
    data['color'] = data['ratingtype'].map(color_code)
    return data

data = load_data(data)

# data_loading.text('loading data...(using st.cache_data)!')
dynamic_filters = DynamicFilters(data, filters=['state', 'premisetype'])
st.sidebar.header("Filter by review type:")
with st.sidebar:
    dynamic_filters.display_filters()

filtered_data = dynamic_filters.filter_df()
if filtered_data not in st.session_state:
    st.session_state.filtered_data = filtered_data



col_1, col_2= st.columns(2)


with col_1:

    st.metric(value=filtered_data['ghgemissionsscope123withrenewableelectricity'].mean(), label = 'Greenhouse Gas Emissions(with renewable energy)')
    
    energy_filter = ['energy','electricity', 'aaa','gas','diesel','rei','kwh']
    environment_filter = ['ieq','thermal','air','acoustic','lighting','office','apartment','bed','rooms','shopping']
    waste_filter = ['waste','recycle']
    water_filter = ['water']
    st.subheader('distribution plot of energy star rating value vs energy star rating value without green power')
    dist_plot_data = filtered_data[['energystarratingvalue', 'energygpstarratingvaluenogp']].dropna()

    fig = ff.create_distplot([dist_plot_data[c] for c in dist_plot_data.columns], dist_plot_data.columns, bin_size=.25)
    st.plotly_chart(fig, use_container_width=True)
    box_plot_data = filtered_data[['ratedgas','rateddiesel','ratedelectricity','premisetype','state']]


result = filtered_data.groupby('certificatevalidto')['energystarratingvalue'].mean().reset_index()
st.subheader('Scatter/Histogram plot of Energy Star ratings to certification validation date')
fig = px.scatter(result, x='certificatevalidto',y='energystarratingvalue',marginal_x="histogram", marginal_y="rug")
fig.update_layout(
    xaxis_title='Carbon Neutral Expiry Date',
    yaxis_title='Rating Value',
    height=600,  
    width=1500    
)
st.plotly_chart(fig)

with col_2:
    st.metric(value=filtered_data['ghgemissionsscope123withoutrenewableelectricity'].mean(), label = 'Greenhouse Gas Emissions(without renewable energy)')
    st.subheader('violin plot of rei related KPIs')
    data = filtered_data[['nonrenewableelectricity_rei%',
    'onsiterenewableelectricity_rei%',
    'retandstateterritorytargets_rei%',
    'greenpower_rei%',
    'othervoluntarypurchases_rei%']]
    fig = px.violin(data)
    st.plotly_chart(fig)
    # st.subheader('Renewable Energy Index')
    # fig = ff.create_bullet(data)
    # st.plotly_chart(fig,use_container_width=True)






# with col_2:
#     # st.subheader('Premisetype barchart!')
#     # z3 = data['PremiseType']
#     # st.plotly_chart(px.bar(z3))
#     z4 = data[['PremiseType','State']]
#     st.subheader('stacked barchart, state and premisetype!')
#     st.plotly_chart(px.bar(z4,x='State',color='PremiseType',barmode='stack',hover_data=['PremiseType']))
#     

#     energy_filter = ['energy','electricity', 'aaa','gas','diesel','rei','kwh']
#     environment_filter = ['ieq','thermal','air','acoustic','lighting','office','apartment','bed','rooms','shopping']
#     waste_filter = ['waste','recycle']
#     water_filter = ['water']

#     energy_cols = [i for i in col_list if any(keyword in i for keyword in energy_filter)]
#     environment_cols = [i for i in col_list if any(keyword in i for keyword in environment_filter)]
#     waste_cols = [i for i in col_list if any(keyword in i for keyword in waste_filter)]
#     water_cols = [i for i in col_list if any(keyword in i for keyword in water_filter)]

#     dict_test = {'energy':len(energy_cols), 'social': len(environment_cols), 'waste':len(waste_cols), 'water': len(water_cols)}

#     st.subheader('KPI count per report category!')
#     st.plotly_chart(px.pie(names=list(dict_test.keys()),values= list(dict_test.values())),title='KPI count per report category')