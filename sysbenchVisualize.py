import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
import re
import plotly.graph_objects as go
import time
import random


# 将sysbench的output输出到一个文件
sysbenchOutputFilePath = 'a.txt'

# 看情况改一下函数：extract()、skipLine()


app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in millixonds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    # lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    # style = {'padding': '5px', 'fontSize': '16px'}
    return [
        # html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        # html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        # html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):

    # 横坐标
    x = []
    # 纵坐标
    y = []

    f = open(sysbenchOutputFilePath)
    lines = f.readlines()

    def extract1(line):
        try:
            x = re.findall('\[\s*(\d+)s\s*\]', line)[0]
            y = re.findall(' tps:\s*(\d+.\d+)', line)[0]
            x = float(x)
            y = float(y)
            return (x, y) 
        except Exception as e:
            print('extract1')
            print('line:' + line)
            print(e)
            return ()

    def extract2(line):
        try:
            x = re.findall('\[\s*(\d+)s\s*\]', line)[0]
            y = re.findall(' reads:\s*(\d+.\d+)', line)[0]
            x = float(x)
            y = float(y)
            return (x, y) 
        except Exception as e:
            print('extract2')
            print(line)
            return ()



    def skipLine(line):
        try:
            if len(line)==0:
                return True
            if not '[' in line:
                return True
            return False
        except Exception as e:
            print('skipLine')
            print(line)
            print(e)
            raise



    for line in lines:
        if skipLine(line):
            continue
        a = extract1(line)
        if a == ():
            continue
        x.append(a[0])
        y.append(a[1])

    print(x)
    print(y)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, 
        y=y, 
        name='TPS',
        line=dict(color='firebrick', width=4)
        ))


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)