"""
https://www.datacamp.com/community/tutorials/learn-build-dash-python

"""
import os
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

#unique_species = 'SELECT DISTINCT spc_common'
#unique_boro = 'SELECT DISTINCT boroname'
health_boro_species = 'SELECT spc_common, boroname, steward, health, COUNT(*) GROUP BY spc_common, boroname, steward, health  LIMIT 100 OFFSET 0'


def call_soql(query, url='https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$query='):
    soql_url = "".join([url, query]).replace(' ', '%20')
    return pd.read_json(soql_url)

#def make_options(query):
#    options = call_soql(query)
#    return ['All'] + sorted(list(set([str(u[0]) for u in options.values])))

#all_options = {
#    'Borough': make_options(unique_boro),
#    'Species': make_options(unique_species)
#}

df = call_soql(health_boro_species)
#  Reorder
df = df[['spc_common', 'boroname', 'steward', 'health', 'COUNT']]
# Rename
df.columns = ['Species', 'Borough', 'Stewards', 'Health', 'Count']
# Na's / Unknown values not required by spec
# df.fillna("Unknown", inplace=True)
df.dropna(subset=['Health'], inplace=True)
# Calculate Percentage of total counts
df['Perc (%)'] = 100 * (df['Count'] / df['Count'].sum())

table_markdown_text ='''
# Data 608: Assignment 4
Jenkins

For each Species and Borough:

1. Measure the proportion of trees in good, fair, or poor health
2. Evaluate the impact of Stewards on tree health


### Notes:

* This web page is based on New York City tree census data: https://data.cityofnewyork.us/Environment/2015-Street-Tree-Census-Tree-Data/uvpi-gqnh
* This app currently has a limit of 1000 results, however, the actual counts-grouped data does not currently exceed this.

### References:
* https://dash.plotly.com/datatable/interactivity
* https://www.datacamp.com/community/tutorials/learn-build-dash-python

## Health and Stewardship Table by Tree Species and Borough
This table is built for Arborists to investigate and filter Health and Stewardship by Species and Borough. The table is sortable and has free text filters which update the table and barcharts below it.
'''

graph_markdown_text ='''
## Bar Charts of Tree Counts for Boroughs, Species, Stewards, and Health
These graphs are filterable based on free-text Table selections.

'''

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([

    dcc.Markdown(children=table_markdown_text),
    html.Div(
        className="row",
        children=[
            html.Div(
                dash_table.DataTable(
                    id='table-paging-with-graph',
                    columns=[
                        {"name": i, "id": i} for i in df.columns
                    ],
                    page_current=0,
                    page_size=1000,
                    page_action='custom',

                    filter_action='custom',
                    filter_query='',

                    sort_action='custom',
                    sort_mode='multi',
                    sort_by=[]
                ),
                style={'height': 750, 'overflowY': 'scroll'},
                className='six columns'
            ),
            dcc.Markdown(children=graph_markdown_text),
            html.Div(
                id='table-paging-with-graph-container',
                className="six columns"
            )
        ]
    )
])

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    Output('table-paging-with-graph', "data"),
    [Input('table-paging-with-graph', "page_current"),
     Input('table-paging-with-graph', "page_size"),
     Input('table-paging-with-graph', "sort_by"),
     Input('table-paging-with-graph', "filter_query")])
def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = df
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )
    # Update Percentages per filters
    dff['Perc (%)'] = 100*(dff['Count'] / dff['Count'].sum())

    return dff.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')


@app.callback(
    Output('table-paging-with-graph-container', "children"),
    [Input('table-paging-with-graph', "data")])
def update_graph(rows):
    dff = pd.DataFrame(rows)
    return html.Div(
        [
            dcc.Graph(
                id=column,
                figure={
                    "data": [
                        {
                            "x": dff[column] if column in dff else [],
                            "y": dff["Count"],
                            "type": "bar",
                            "marker": {"color": "#0074D9"},
                        }
                    ],
                    "layout": {
                        "title": "Filtered " + str(column) + " counts",
                        "xaxis": {"automargin": True},
                        "yaxis": {"automargin": True},
                        "height": 250,
                        "margin": {"t": 50, "l": 10, "r": 10},
                    },
                },
            )
            for column in ["Borough", "Species", "Stewards", "Health"]
        ]
    )


if __name__ == '__main__':
    app.run_server(debug=True)
