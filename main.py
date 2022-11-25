
import pandas as pd
import numpy as np
from datetime import timedelta
from colour import Color
import altair as alt 

# Loading DF
df_pred = pd.read_csv("/content/drive/My Drive/phd/notebooks/visual_survey/predictions_211117.csv")
df_pred=np.expm1(df_pred)
df_pred.columns = (df_pred.columns.astype(int)+1).astype(str)
preds = df_pred.values

# Adding helper columns
df_pred["h"]=df_pred.index

df_pred["h1"]=df_pred["h"]-.5
df_pred["h2"]=df_pred["h"]+.5

df_pred["hsbl"]=df_pred["h"]-.2
df_pred["hsbh"]=df_pred["h"]+.2

df_pred["hbbl"]=df_pred["h"]-.4
df_pred["hbbh"]=df_pred["h"]+.4

df_pred["hour"] = pd.date_range('2017-11-21 11:00', '2017-11-22 09:00', freq='H')

df_pred["hour1"]=df_pred["hour"]-timedelta(minutes=30)
df_pred["hour2"]=df_pred["hour"]+timedelta(minutes=30)

df_pred["hoursbl"]=df_pred["hour"]-timedelta(minutes=10)
df_pred["hoursbh"]=df_pred["hour"]+timedelta(minutes=10)

df_pred["hourbbl"]=df_pred["hour"]-timedelta(minutes=20)
df_pred["hourbbh"]=df_pred["hour"]+timedelta(minutes=20)

# Color Scale
red = Color("#c6e3f9")
blue = Color("#B19CD9")
colors = list(red.range_to(blue, 50))

# Confidence Interval
total_chart = alt.Chart(df_pred).mark_line().encode(
    x=alt.X('yearmonthdatehours(hour):O',title="Time of Day",axis=alt.Axis(grid=True)),
    y=alt.Y('50',scale=alt.Scale(zero=False),title="NO2 level"),
    color=alt.value("lightblue")
)+\
alt.Chart(df_pred).mark_line().encode(
    x=alt.X('h', axis=alt.Axis(labels=False),title=""),
    y=alt.Y('5',scale=alt.Scale(zero=False),title="")
)+\
alt.Chart(df_pred).mark_line().encode(
    x=alt.X('h', axis=alt.Axis(labels=False),title=""),
    y=alt.Y('95',scale=alt.Scale(zero=False),title="")
)
total_chart.title = 'NO2 prediction levels - Confidence interval'
total_chart.width = 600
total_chart.save("ci_chart.html")
total_chart

# Gradient
cdf = pd.DataFrame()
cdf["color"]=list(map(lambda e:e.get_hex(),colors))+list(reversed(list(map(lambda e:e.get_hex(),colors))))
cdf["range"]=  cdf.index
rangelabel = alt.Chart(cdf[cdf["range"]%5==0]).mark_rect().encode(
    y=alt.Y("range:N",sort='descending',title="",axis=alt.Axis(orient="right")),
    tooltip="range",
    color=alt.Color("range:N",scale=alt.Scale(range=cdf["color"][cdf["range"]%5==0].values), legend=None)
).properties(
    height=250
)
rangelabel

charts = []
for i in np.arange(1,50,5):
  charts.append(alt.Chart(df_pred).mark_area().encode(
    x=alt.X('yearmonthdatehours(hour):O',title="Time of Day",axis=alt.Axis(grid=True)),
    y=alt.Y(str(i),scale=alt.Scale(zero=False),title="NO2 level"),
    y2=alt.Y2(str(100-i)),
    color=alt.value(colors[i].get_hex())
  ))
total_chart = sum(charts)
total_chart.title = 'NO2 prediction levels - Gradient Chart'
total_chart.width = 600
total_chart

(total_chart|rangelabel).save("chart_gradient_230417.html")

t=alt.layer( 

alt.Chart(df_pred).mark_rule().encode(
    x=alt.X('yearmonthdatehours(hour):O',axis=alt.Axis(labels=True,grid=False,orient="top",ticks=True,labelExpr="isDate(datum.value) ? datum.label : '' "),title=""),
    y=alt.Y('1',scale=alt.Scale(zero=False),title="NO2 level"),
    y2=alt.Y2("99")
),

alt.Chart(df_pred).mark_rect().encode(
    x=alt.X('hoursbl',title=""),
    x2='hoursbh',
    y=alt.Y('10',scale=alt.Scale(zero=False),title=""),
    y2=alt.Y2("90")
)

)

# EPS Gram
total_chart=alt.Chart(df_pred).mark_rule().encode(
    x=alt.X('yearmonthdatehours(hour):O',axis=alt.Axis(labels=False,grid=False,orient="top",labelExpr="isDate(datum.value) ? datum.label : '' "),title=""),
    y=alt.Y('1',scale=alt.Scale(zero=False),title="NO2 level"),
    y2=alt.Y2("99")
)+\
alt.Chart(df_pred).mark_rect().encode(
    x=alt.X('hoursbl',axis=alt.Axis(labels=False,orient="top",grid=False),title=""),
    x2='hoursbh',
    y=alt.Y('10',scale=alt.Scale(zero=False),title=""),
    y2=alt.Y2("90")
)+\
alt.Chart(df_pred).mark_rect().encode(
    x=alt.X('hourbbl',axis=alt.Axis(labels=False,orient="top",grid=False),title=""),
    x2='hourbbh',
    y=alt.Y('25',scale=alt.Scale(zero=False),title=""),
    y2=alt.Y2("75")
)+\
alt.Chart(df_pred).mark_rect().encode(
    x=alt.X('hour1',axis=alt.Axis(labels=False,orient="top",grid=False),title=""),
    x2='hour2',
    y=alt.Y('50',scale=alt.Scale(zero=False),title=""),
    y2=alt.Y2('51'),
    color=alt.value("white")
)+\
alt.Chart(df_pred).mark_rect().encode(
    x=alt.X('yearmonthdatehours(hour):O',title="Time of Day",axis=alt.Axis(orient="bottom",grid=False,labels=True,labelExpr="isDate(datum.value) ? datum.label : '' ")),
    y=alt.value(0),
    opacity=alt.value(0)
)

total_chart.title = 'NO2 prediction levels - Box Plot Chart'
total_chart.width = 600
total_chart.save("chart_box_211117.html")
total_chart

# Time Series Natural Frequency Chart
charts = []
for i in np.arange(5,96,10):
  charts.append(alt.Chart(df_pred).mark_point().encode(
    x=alt.X('yearmonthdatehours(hour):O',title="Time of Day",axis=alt.Axis(orient="bottom")),
    y=alt.Y(str(i),scale=alt.Scale(zero=False),title="NO2 level")
  ))
total_chart = sum(charts)
total_chart+=alt.Chart(df_pred).mark_line().encode(
    x=alt.X('yearmonthdatehours(hour):O',title="Time of Day",axis=alt.Axis(grid=True)),
    y=alt.Y('50',scale=alt.Scale(zero=False),title="NO2 level"),
    color=alt.value("lightblue")
)

total_chart.title = 'NO2 prediction levels - Dot Chart'
total_chart.width = 600
