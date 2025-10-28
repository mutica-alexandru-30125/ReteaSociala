from dash import html, dcc
import dash_cytoscape as cyto
from styles import card_style, button_style, input_style, radio_container_style

def create_layout():
    return html.Div([
        html.H3("Social Network Graph Builder", style={"textAlign": "center", "color": "#333", "marginBottom": "20px"}),
        html.Div([
            html.Div([
                html.H4("Graph Options"),
                dcc.Input(id="num-nodes", type="number", min=1, step=1, placeholder="Number of nodes", style=input_style),
                html.Button("Generate", id="btn-generate", n_clicks=0, style=button_style),
                html.Button("Generate Random Graph", id="btn-random", n_clicks=0, style=button_style),
                html.Button("Add New Node", id="btn-add-node", n_clicks=0, disabled=True, style=button_style),
            ], style=card_style),
            html.Div([
                html.H4("Mode"),
                html.Div([
                    html.Div([
                        dcc.RadioItems(
                            id="mode-toggle",
                            options=[
                                {"label": "Connect Mode", "value": "connect"},
                                {"label": "Add Data Mode", "value": "data"},
                                {"label": "Delete Mode", "value": "delete"}
                            ],
                            value="connect",
                            style={"margin": "0"}
                        )
                    ], style=radio_container_style)
                ], style={"marginTop": "10px"}),
                html.Button("Analyse", id="btn-analyse", n_clicks=0, style=button_style)
            ], style=card_style),
            html.Div([
                html.H4("Edge Types"),
                dcc.RadioItems(
                    id="edge-type-radio",
                    options=[
                        {"label": "Friend", "value": "friend"},
                        {"label": "Close Friend", "value": "close_friend"},
                        {"label": "Work Colleagues", "value": "work_colleagues"},
                        {"label": "Family", "value": "family"},
                        {"label": "Acquaintance", "value": "acquaintance"}
                    ],
                    value="friend",
                    style={"margin": "0"}
                ),
                html.Div([
                    html.Span("Friend", style={"marginRight": "10px", "display": "inline-block"}),
                    html.Span(style={"backgroundColor": "#00b894", "width": "15px", "height": "15px", "display": "inline-block", "marginRight": "20px", "border": "1px solid #000"}),
                    html.Span("Close Friend", style={"marginRight": "10px", "display": "inline-block"}),
                    html.Span(style={"backgroundColor": "#00cec9", "width": "15px", "height": "15px", "display": "inline-block", "marginRight": "20px", "border": "1px solid #000"}),
                    html.Span("Work Colleagues", style={"marginRight": "10px", "display": "inline-block"}),
                    html.Span(style={"backgroundColor": "#fdcb6e", "width": "15px", "height": "15px", "display": "inline-block", "marginRight": "20px", "border": "1px solid #000"}),
                    html.Span("Family", style={"marginRight": "10px", "display": "inline-block"}),
                    html.Span(style={"backgroundColor": "#e17055", "width": "15px", "height": "15px", "display": "inline-block", "marginRight": "20px", "border": "1px solid #000"}),
                    html.Span("Acquaintance", style={"marginRight": "10px", "display": "inline-block"}),
                    html.Span(style={"backgroundColor": "#a29bfe", "width": "15px", "height": "15px", "display": "inline-block", "border": "1px solid #000"}),
                ], style={"marginTop": "10px", "display": "flex", "flexWrap": "wrap", "justifyContent": "center"})
            ], style=card_style),
        ], style={"display": "flex", "flexWrap": "wrap", "justifyContent": "center", "marginBottom": "20px"}),
        cyto.Cytoscape(
            id="graph",
            elements=[],
            layout={"name": "preset"},  # preserve node positions so user drag is kept
            style={"width": "100%", "height": "600px", "border": "1px solid #ccc", "borderRadius": "8px"},
            userPanningEnabled=True,
            userZoomingEnabled=True,
            boxSelectionEnabled=False,
            autoungrabify=False,  # allow user to grab and move nodes
            stylesheet=[
                {"selector": "node", "style": {
                    "label": "data(label)",
                    "background-color": "#74b9ff",
                    "width": "80px",
                    "height": "80px",
                    "text-valign": "center",
                    "font-size": "14px",
                    "border-width": 2,
                    "border-color": "#0984e3"
                }},
                {"selector": "node.selected", "style": {
                    "background-color": "#ff7675",
                    "border-color": "#d63031"
                }},
                {"selector": "edge[type='friend']", "style": {
                    "line-color": "#00b894",
                    "width": 3
                }},
                {"selector": "edge[type='close_friend']", "style": {
                    "line-color": "#00cec9",
                    "width": 4
                }},
                {"selector": "edge[type='work_colleagues']", "style": {
                    "line-color": "#fdcb6e",
                    "width": 3
                }},
                {"selector": "edge[type='family']", "style": {
                    "line-color": "#e17055",
                    "width": 3
                }},
                {"selector": "edge[type='acquaintance']", "style": {
                    "line-color": "#a29bfe",
                    "width": 2
                }}
            ]
        ),
        html.Div(id="info", style={"marginTop": "10px", "color": "#28a745", "textAlign": "center", "fontSize": "18px"}),
        html.Div(id="analysis", style={"marginTop": "10px", "textAlign": "center"}),
        dcc.Store(id="selected-node", data=None),  # store the selected node id
        dcc.Store(id="adding-new", data=False),  # store if adding new node
        dcc.Store(id="edge-type", data="friend"),  # store selected edge type
        # Tooltip for node details on hover, positioned in top-right corner
        html.Div(id="tooltip", children="Hover over a node to see details.", style={"position": "fixed", "top": "10px", "right": "10px", "background": "white", "border": "1px solid black", "padding": "5px", "zIndex": 1000, "pointerEvents": "none", "display": "block", "borderRadius": "5px"}),
        # Modal for editing node data (using html.Div with conditional display)
        html.Div(
            id="node-modal",
            children=[
                html.Div([
                    html.H4("Add/Edit Node Data"),
                    html.Label("Name:"),
                    dcc.Input(id="name-input", type="text", placeholder="Enter name"),
                    html.Label("Age:"),
                    dcc.Input(id="age-input", type="number", placeholder="Enter age"),
                    html.Label("Occupation:"),
                    dcc.Input(id="occupation-input", type="text", placeholder="Enter occupation"),
                    html.Button("Save", id="save-btn", n_clicks=0, style=button_style),
                    html.Button("Cancel", id="cancel-btn", n_clicks=0, style={**button_style, "backgroundColor": "#6c757d"}),
                ], style={"padding": "20px", "backgroundColor": "white", "border": "1px solid #ccc", "position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)", "zIndex": 1000, "borderRadius": "8px", "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"})
            ],
            style={"display": "none"}  # hidden by default
        )
    ], style={"backgroundColor": "#f8f9fa", "minHeight": "100vh", "padding": "20px"})