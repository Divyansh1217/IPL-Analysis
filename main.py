import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

import chart_studio.plotly as py
from plotly import tools
from plotly.offline import init_notebook_mode
import plotly.figure_factory as ff
import plotly.graph_objs as go

sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")

# To remove un-necessary warnings
import warnings
warnings.filterwarnings("ignore")

deliveries = pd.read_csv('deliveries.csv')
matches = pd.read_csv('matches.csv')
z=st.selectbox("Select dataset to show",("Full Delieveries","Full Matches","First 10 row Deliveries","First 1o row Matches"),index=None,placeholder="Select Dataset")
if z=="Full Delieveries":
    st.write(deliveries)
elif z=="Full Matches":
    st.write(matches)
elif z=="First 10 row Deliveries":
    st.write(deliveries.head(10))
else:
    st.write(matches.head(10))

x=['Sunrisers Hyderabad', 'Mumbai Indians', 'Gujarat Lions',
    'Rising Pune Supergiant', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Delhi Daredevils', 'Kings XI Punjab',
    'Chennai Super Kings', 'Rajasthan Royals', 'Deccan Chargers',
    'Kochi Tuskers Kerala', 'Pune Warriors', 'Rising Pune Supergiants', 'Delhi Capitals','Lucknow Super Giants','Royal Challengers Bengaluru']

y = ['SRH','MI','GL','RPS','RCB','KKR','DC','KXIP','CSK','RR','SRH','KTK','PW','RPS','DC',"LSG",'RCB']
deliveries.rename(columns={'match_id': 'id'}, inplace=True)
matches.replace(x,y,inplace = True)
deliveries.replace(x,y,inplace = True)
x=['Punjab Kings']
y=['KXIP']
matches.replace(x,y,inplace = True)
deliveries.replace(x,y,inplace = True)
matches_played=pd.concat([matches['team1'],matches['team2']])
matches_played=matches_played.value_counts().reset_index()
matches_played.columns=['Team','Total Matches']
matches_played['wins']=matches['winner'].value_counts().reset_index()['winner']

matches_played.set_index('Team',inplace=True)
totm = matches_played.reset_index().head(8)
batsmen = matches[['id','season']].merge(deliveries, left_on = 'id', right_on = 'id', how = 'left').drop('id', axis = 1)
season=batsmen.groupby(['season'])['total_runs'].sum().reset_index()
def Total():
    matches['season'] = matches['date'].str[:4].astype(int)
    data = [go.Histogram(x=matches['season'], marker=dict(color='#EB89B5', line=dict(color='#000000', width=1)), opacity=0.75)]
    layout = go.Layout(title='Matches In Every Season ',xaxis=dict(title='Season',tickmode='linear'),
                        yaxis=dict(title='Count'),bargap=0.2, plot_bgcolor='rgb(245,245,245)')

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart((fig))
def TMPW():
    trace = go.Table(
        header=dict(values=["Team","Total Matches","Wins"],
                    fill = dict(color='#ff96ea'),
                    font = dict(color=['rgb(45, 45, 45)'] * 5, size=14),
                    align = ['center'],
                height = 30),
        cells=dict(values=[totm['Team'], totm['Total Matches'], totm['wins']],
                fill = dict(color=['rgb(235, 193, 238)', 'rgba(228, 222, 249, 0.65)']),
                align = ['center'], font_size=13, height=25))

    layout = dict(
        width=750,
        height=420,
        autosize=False,
        title='Total Matches vs Wins per team',
        margin = dict(t=100),
        showlegend=False,    
    )

    fig1 = dict(data=[trace], layout=layout)
    st.plotly_chart(fig1)
def PAIT():
    trace1 = go.Bar(x=matches_played.index,y=matches_played['Total Matches'],
                name='Total Matches',opacity=0.4)

    trace2 = go.Bar(x=matches_played.index,y=matches_played['wins'],
                    name='Matches Won',marker=dict(color='red'),opacity=0.4)

    trace3 = go.Bar(x=matches_played.index,
                y=(round(matches_played['wins']/matches_played['Total Matches'],3)*100),
                name='Win Percentage',opacity=0.6,marker=dict(color='gold'))

    data = [trace1, trace2, trace3]

    layout = go.Layout(title='Match Played, Wins And Win Percentage',xaxis=dict(title='Team'),
                    yaxis=dict(title='Count'),bargap=0.2,bargroupgap=0.1, plot_bgcolor='rgb(245,245,245)')

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)
def Venue_P():
    venue_matches=matches.groupby('venue').count()[['id']].sort_values(by='id',ascending=False).head()
    ser = pd.Series(venue_matches['id']) 
    venue_matches=matches.groupby('venue').count()[['id']].reset_index()

    data = [{"y": venue_matches['id'],"x": venue_matches['venue'], 
            "marker": {"color": "lightblue", "size": 12},
            "line": {"color": "red","width" : 2,"dash" : 'dash'},
            "mode": "markers+lines", "name": "Women", "type": "scatter"}]

    layout = {"title": "Stadiums Vs. Matches", 
            "xaxis": {"title": "Matches Played", }, 
            "yaxis": {"title": "Stadiums"},
            "autosize":False,"width":900,"height":700,"plot_bgcolor":"rgb(245,245,245)"}

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)
def Toss():
    data = [go.Bar(
    x = matches["toss_decision"].value_counts().index,
    y = matches["toss_decision"].value_counts().values,
    marker = dict(line=dict(color='#000000', width=1))
    )]

    layout = go.Layout(
    {
        "title":"Most Likely Decision After Winning Toss",
        "xaxis":dict(title='Decision'),
        "yaxis":dict(title='Number of Matches'),
        "plot_bgcolor":'rgb(245,245,245)'
    }
    )
    fig = go.Figure(data=data,layout = layout)
    st.plotly_chart(fig)
def Rps():
    avgruns_each_season = matches.groupby(['season']).count().reset_index()
    avgruns_each_season.rename(columns={'id': 'matches'}, inplace=True)
    avgruns_each_season['total_runs'] = season['total_runs']
    avgruns_each_season['average_runs_per_match'] = avgruns_each_season['total_runs'] / avgruns_each_season['matches']
    fig = go.Figure()
    fig2=go.Figure()
    fig2.add_trace(go.Scatter(
        x=avgruns_each_season['season'],
        y=avgruns_each_season['average_runs_per_match'],
        mode='lines',
        marker=dict(size=10, color='blue'),
        name='Average Runs per Match'))
    fig.add_trace(go.Scatter(
        x=avgruns_each_season['season'],
        y=avgruns_each_season['total_runs'],
        mode='lines',
        line=dict(color='red', width=2),
        name='Total Runs'))
    fig.update_layout(
        title='Total Runs',
        xaxis_title='Season',
        yaxis_title='Total Runs',
        xaxis_tickangle=45,
        template='plotly_white')
    fig2.update_layout(
        title='Average Runs per Match Each Season',
        xaxis_title='Season',
        yaxis_title='Average Runs per Match',
        xaxis_tickangle=45,
        template='plotly_white')
    st.plotly_chart(fig)
    st.plotly_chart(fig2)
def Runs():
    Season_boundaries=batsmen.groupby("season")["batsman_runs"].agg(lambda x: (x==6).sum()).reset_index()
    fours=batsmen.groupby("season")["batsman_runs"].agg(lambda x: (x==4).sum()).reset_index()
    Season_boundaries=Season_boundaries.merge(fours,left_on='season',right_on='season',how='left')
    Season_boundaries=Season_boundaries.rename(columns={'batsman_runs_x':'6"s','batsman_runs_y':'4"s'})

    Season_boundaries['6"s'] = Season_boundaries['6"s']*6
    Season_boundaries['4"s'] = Season_boundaries['4"s']*4
    Season_boundaries['total_runs'] = season['total_runs']

    trace1 = go.Bar(
        x=Season_boundaries['season'],
        y=Season_boundaries['total_runs']-(Season_boundaries['6"s']+Season_boundaries['4"s']),
        marker = dict(line=dict(color='#000000', width=1)),
        name='Remaining runs',opacity=0.6)

    trace2 = go.Bar(
        x=Season_boundaries['season'],
        y=Season_boundaries['4"s'],
        marker = dict(line=dict(color='#000000', width=1)),
        name='Run by 4"s',opacity=0.7)

    trace3 = go.Bar(
        x=Season_boundaries['season'],
        y=Season_boundaries['6"s'],
        marker = dict(line=dict(color='#000000', width=1)),
        name='Run by 6"s',opacity=0.7)


    data = [trace1, trace2, trace3]
    layout = go.Layout(title="Run Distribution per year",barmode='stack',xaxis = dict(tickmode='linear',title="Year"),
                                        yaxis = dict(title= "Run Distribution"), plot_bgcolor='rgb(245,245,245)')

    fig = go.Figure(data=data, layout=layout)
    st.plotly_chart(fig)
def Runsbyteam():
    high_scores=deliveries.groupby(['id', 'inning','batting_team','bowling_team'])['total_runs'].sum().reset_index() 
    high_scores=high_scores[high_scores['total_runs']>=200]
    hss = high_scores.nlargest(10,'total_runs')

    trace = go.Table(
        header=dict(values=["Inning","Batting Team","Bowling Team", "Total Runs"],
                    fill = dict(color = 'red'),
                    font = dict(color = 'black', size = 14),
                    align = ['center'],height = 30),
        cells=dict(values=[hss['inning'], hss['batting_team'], hss['bowling_team'], hss['total_runs']],
                fill = dict(color = ['blueviolet', 'rgb(245, 0, 0)']),
                align = ['center'], font_size=13))

    layout = dict(
        width=830,
        height=410,
        autosize=False,
        title='Highest scores of IPL',
        showlegend=False,    
    )

    fig1 = dict(data=[trace], layout=layout)
    st.plotly_chart(fig1)




x=st.selectbox("Select the Analysis",("Total matches","Total Win and Matches","Percentage of wins","Venue played","Match win after Toss","Runs per match","No of 6's,4's,0's","Runs by Teams"))

if x=="Total matches":
    Total()
elif x=="Total Win and Matches":
    TMPW()
elif x=="Percentage of wins":
    PAIT()
elif x=="Venue played":
    Venue_P()
elif x=="Match win after Toss":
    Toss()
elif x=="Runs per match":
    Rps()
elif x=="No of 6's,4's,0's":
    Runs()
elif x=="Runs by Teams":
    Runsbyteam()


