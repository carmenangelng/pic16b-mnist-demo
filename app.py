from dash import Dash, dcc, html, dash_table, Input, Output, State, callback, no_update

import base64
import datetime
import io

import pandas as pd
import numpy as np
import sklearn
import pickle
from plotly import express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(figure={}, id='output-fig'),
    html.Div(id='output-prediction')
    
])

# Three outputs, one input, two states (taken from the uploaded data)
@callback(Output('output-data-upload', 'children'),
                Output('output-fig', 'figure'),
                Output('output-prediction', 'children'),
                Input('upload-data', 'contents'),
                State('upload-data', 'filename'),
                State('upload-data', 'last_modified'))
def update_output(content, name, date):
    if content is not None:
        children, fig, digit = parse_contents(content, name, date) 
        return children, fig, digit
    else: 
        # default values with empty image
        return (None, px.imshow(np.zeros((8, 8)), range_color=(0, 16), color_continuous_scale="Greys"), None)
    

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'txt' in filename:
            # Step 1: loading the image
            arr = np.loadtxt(
                io.StringIO(decoded.decode('utf-8')))
            
            # Step 2: loading the picked model
            model = pickle.load(open('model.pkl', 'rb'))
            
            # Step 3: running a ML model on the image
            # Step 4: store the ML model's prediction in some Python variable
            x = arr.reshape(1, 64)
            digit = model.predict(x)[0]
        
            return (
                html.Div(str(arr)),
                # Step 5: Show the image
                px.imshow(arr, range_color=(0, 16), color_continuous_scale="Greys"),
                # Step 6: Print the prediction and some message
                html.Div(f"This looks like a {digit}!")
            )
            
    except Exception as e:
        print(e)
        return (html.Div([
            'There was an error processing this file.'
        ]),
        px.imshow(np.zeros((8, 8)), range_color=(0, 16), color_continuous_scale="Greys"),
        None)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
