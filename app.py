import constants as c
import data_preparation as dp
from data_preparation import services_dataset as dataset
import dash_cytoscape as cyto
from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)

# elements = dp.generate_data_for_graph(dataset)
cyto.load_extra_layouts()

default_stylesheet = [{
    "selector": "node",
    "style": {
        'shape': 'roundrect',
        'width': 25,
        'height': 15,
        'background-fit':'cover',
        'background-opacity': 0,
        'background-clip': 'none',
        'background-image': 'data(url)',
        "label": "data(label)",
        "color": "black",
        "text-opacity": 1,
        'font-size': '4px',
        "font-weight": "normal",
        "text-transform": "none",
        "text-wrap": "wrap",
        #"text-halign": "center",
        "text-valign": "bottom",
    }
}]

app.layout = html.Div([
    dcc.Dropdown(
        id='capability_dropdown',
        options=[
            {'label': capability, 'value': capability}
            for capability in dp.get_capabilities(dataset, 3)
        ],
        value=dp.get_capabilities(dataset, 3)[0]
    ),
    html.Div(
        id='cyto_container',
        children=[
            cyto.Cytoscape(
                id='stk_diagram',
                # elements=elements,
                style={'width': '100%', 'height': '550px'},
                # layout=layout,
                stylesheet=default_stylesheet
            )
        ]
    ),
    html.Div([
        html.H3('Exchanged Services'),
        html.Div(
            id='services'
        )
    ])
    
])

@app.callback(
    Output('services', 'children'),
    Input('capability_dropdown', 'value'),
    Input('stk_diagram', 'tapEdgeData'),
    Input('stk_diagram', 'selectedEdgeData')
)
def add_service_list(capability, data, selected_data):
    if data and selected_data:
        filtered_dataset = dataset[
            dataset[c.SOURCE_STK].eq(data['source']) &
            dataset[c.TARGET_STK].eq(data['target']) &
            dataset[c.L3_CAP].eq(capability)
        ]
        
    else:
        filtered_dataset = dataset[
            dataset[c.L3_CAP].eq(capability)
        ]
    return [
            html.P([
                html.Img(
                    src='https://atmmasterplan.eu/assets/icons/svc-5222731c20f214efa1df94cd374d6a0ecd0237714f2a5d01e3b741c7c744db20.png',
                    style={
                        'width': '2rem',
                        'verticalAlign': 'middle',
                        'marginRight': '5px'}
                ),
                service
            ])
            for service in sorted(list(filtered_dataset[c.SVC].unique()))
        ]
        


@app.callback(
    Output('stk_diagram', 'elements'),
    Output('stk_diagram', 'layout'),
    # Output('cyto_container', 'children'),
    Input('capability_dropdown', 'value')
)
def update_data_in_diagram(capability):
    filtered_dataset = dataset[dataset[c.L3_CAP].eq(capability)]
    elements = dp.generate_data_for_graph(filtered_dataset)
    if len(elements) > 30:
        layout = {'name': 'circle'}
    else:
        layout = {'name': 'cose'}
    """
    return cyto.Cytoscape(
        id='stk_diagram',
        elements=elements,
        style={'width': '100%', 'height': '550px'},
        layout=layout,
        stylesheet=default_stylesheet
    )
    """
    return elements, layout
    

    # return dp.generate_data_for_graph(filtered_dataset)

if __name__ == '__main__':
    app.run_server(debug=True)

