"""This file mimics the behavior in python_flask/app.py in running the flask server."""
from flask import Flask, request
from io import StringIO, BytesIO
import pandas as pd
from matplotlib.figure import Figure
import base64
import json

app = Flask(__name__)

def display_graph(df):
    """Method that will generate and display a graph to the html page."""
    fig = Figure()
    ax = fig.subplots()
    ax.plot(df)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode('ascii')
    return data


@app.route('/transfer', methods=['POST'])
def upload_file():
    #return "Hello, World"
    data = request.data
    s=str(data,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)
    # line_graph = display_graph(df)
    return json.dumps(df.to_json())
    # return df.to_html


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8001)