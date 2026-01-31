# project using streamlit and plotly
import streamlit as st
import plotly.express as px
import pandas as pd

def mean_growth_rate(initial_period, 
                     final_period,
                     df):
    if final_period - initial_period < 2:
        return (df[str(final_period)] - df[str(initial_period)]) / df[str(initial_period)]
    else:
        dates = []
        for year in range(initial_period+1, final_period):
            df['rate' + str(year)] = (df[str(year)] - df[str(year-1)])/ df[str(year -1 )]
            dates.append('rate' + str(year))
        return df[dates].mean(axis=1)

def contribution(year):
  year  = str(year)
  total = df[year].sum()
  return (df[year]/total)*100

url = 'https://raw.githubusercontent.com/it-ces/Datasets/refs/heads/main/Dpto-gdps.csv'

df  =  pd.read_csv(url)
st.header('Inequality income')
st.dataframe(df.head())

G_min_value = 2005
G_max_value = 2020

from_t = st.slider(
      'years',
      min_value = G_min_value,
      max_value = G_max_value,
      value=2005,
      step =1,
     )

until_t = st.slider(
      'years',
      min_value = G_min_value+1,
      max_value = G_max_value-1,
      value=2007,
      step =1,
     )


df['mean rate'] = mean_growth_rate(from_t, until_t,df)



scatter1 = px.scatter(df, x='2005', y='mean rate', 
                      color = '2005',
                      hover_data=['DEPARTAMENTOS'],
                      trendline='ols')
scatter1.update_traces(
    line=dict(color="red", width=3),
    selector=dict(mode="lines")
)

# we can add the parameter size
# the parameter symbol.
st.subheader('beta convergence')

scatter1.update_layout(
    title = f'Mean growth rate ({from_t} - {until_t}) - initial gdp 2005',
    xaxis_title = 'initial gdp 2005',
    yaxis_title = 'mean growth rate'
)
st.plotly_chart(scatter1)





year_contrib = st.slider(
      'contribution year',
      min_value = G_min_value,
      max_value = G_max_value,
      value=2005,
      step =1,
     )

st.subheader('Contribution')


df['temp_contribution'] = contribution(year_contrib)
pie1 = px.pie(df, values = 'temp_contribution', names='DEPARTAMENTOS')
st.plotly_chart(pie1)


# button to create a dataframe with rank!

