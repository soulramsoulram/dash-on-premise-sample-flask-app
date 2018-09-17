from flask import Flask, jsonify
import plotly.graph_objs as go
import pandas as pd
import colorlover as cl
import os

server = Flask(__name__)

def path(partial_path):
    if 'DYNO' in os.environ:
        return partial_path
    return '/{}{}'.format(config.DASH_APP_NAME, partial_path)


@server.route(path('/<boro>/<species>'), methods=['GET'])
def return_pie(boro, species):
    url = ('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?' +
           '$select=health,count(bbl)' +
           '&$where=spc_common=\'{}\'&boroname=\'{}\'' +
           '&$group=health').format(species, boro).replace(' ', '%20')
    trees = pd.read_json(url).dropna()

    data = [
        dict(
            type='pie',
            labels=trees['health'].tolist(),
            values=trees['count_bbl'].tolist(),
            marker=dict(colors=cl.scales['3']['qual']['Set2'])
        )
    ]

    if boro == 'Bronx':
        boro = 'The Bronx'

    layout = dict(title='{} in {}'.format(species, boro))

    fig = dict(data=data, layout=layout)

    return jsonify(fig)


if __name__ == '__main__':
    server.run(debug=True)
