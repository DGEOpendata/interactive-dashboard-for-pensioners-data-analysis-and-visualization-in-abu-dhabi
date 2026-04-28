python
from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__)

def load_data():
    data = pd.read_excel("Distribution_of_Pensioners_2022.xlsx")
    return data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    data = load_data()
    return data.to_json(orient='records')

@app.route('/visualize', methods=['GET'])
def visualize():
    data = load_data()
    chart_type = request.args.get('chart_type', 'bar')
    if chart_type == 'bar':
        fig = px.bar(data, x='Quarter', y='Count', color='Gender', barmode='group', title='Pensioner Distribution by Quarter and Gender')
    elif chart_type == 'line':
        fig = px.line(data, x='Quarter', y='Count', color='Gender', title='Trend of Pensioner Count by Quarter')
    else:
        fig = px.pie(data, names='Gender', values='Count', title='Gender Distribution')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == '__main__':
    app.run(debug=True)
