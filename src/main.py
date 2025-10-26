import random
import dash
from dash import html, dcc, Input, Output, State
import dash_cytoscape as cyto

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3("Create movable nodes"),
    html.Div([
        dcc.Input(id="num-nodes", type="number", min=1, step=1, placeholder="Number of nodes"),
        html.Button("Generate", id="btn-generate", n_clicks=0),
        html.Button("Generate Random Graph", id="btn-random", n_clicks=0),
        html.Button("Add New Node", id="btn-add-node", n_clicks=0),
        html.Label("Mode:", style={"marginLeft": "20px"}),
        dcc.RadioItems(
            id="mode-toggle",
            options=[
                {"label": "Connect Mode", "value": "connect"},
                {"label": "Add Data Mode", "value": "data"}
            ],
            value="connect",
            inline=True
        ),
        html.Label("Edge Type:", style={"marginLeft": "20px"}),
        dcc.RadioItems(
            id="edge-type",
            options=[
                {"label": "Friend", "value": "friend"},
                {"label": "Close Friend", "value": "close_friend"},
                {"label": "Work Colleagues", "value": "work_colleagues"},
                {"label": "Family", "value": "family"},
                {"label": "Acquaintance", "value": "acquaintance"}
            ],
            value="friend",
            inline=True
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
        ], style={"marginTop": "5px"})
    ], style={"marginBottom": "10px"}),
    cyto.Cytoscape(
        id="graph",
        elements=[],
        layout={"name": "preset"},  # preserve node positions so user drag is kept
        style={"width": "100%", "height": "600px", "border": "1px solid #ccc"},
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
    html.Div(id="info", style={"marginTop": "10px", "color": "green"}),
    dcc.Store(id="selected-node", data=None),  # store the selected node id
    dcc.Store(id="adding-new", data=False),  # store if adding new node
    # Tooltip for node details on hover, positioned in top-right corner
    html.Div(id="tooltip", children="Hover over a node to see details.", style={"position": "fixed", "top": "10px", "right": "10px", "background": "white", "border": "1px solid black", "padding": "5px", "zIndex": 1000, "pointerEvents": "none", "display": "block"}),
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
                html.Button("Save", id="save-btn", n_clicks=0),
                html.Button("Cancel", id="cancel-btn", n_clicks=0),
            ], style={"padding": "20px", "backgroundColor": "white", "border": "1px solid #ccc", "position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)", "zIndex": 1000})
        ],
        style={"display": "none"}  # hidden by default
    )
])

def initial_position(num, width=900, height=550, margin=50):
    nodes = []
    if num == 0:
        return nodes
    row1_count = num // 2
    row2_count = num - row1_count
    y1 = height // 4
    y2 = 3 * height // 4
    for i in range(1, num + 1):
        if i <= row1_count:
            x = (i - 1) * (width - 2 * margin) // (row1_count - 1) + margin if row1_count > 1 else width // 2
            y = y1
        else:
            idx = i - row1_count
            x = (idx - 1) * (width - 2 * margin) // (row2_count - 1) + margin if row2_count > 1 else width // 2
            y = y2
        nodes.append({
            "data": {"id": str(i), "label": f"Person {i}"},
            "position": {"x": x, "y": y}
        })
    return nodes

def random_position(width=900, height=550, margin=50):
    return {"x": random.randint(margin, width - margin), "y": random.randint(margin, height - margin)}

def generate_random_graph():
    num_nodes = random.randint(5, 15)
    nodes = []
    names =  ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry", "Ivy", "Jack", "Kate", "Liam", "Mia", "Noah", "Olivia", "Raul", "Michel", "John", "Alex"]
    occupations = ["Engineer", "Teacher", "Doctor", "Artist", "Chef", "Lawyer", "Scientist", "Writer", "Nurse", "Programmer"]
    for i in range(1, num_nodes + 1):
        name = random.choice(names)
        age = random.randint(18, 65)
        occupation = random.choice(occupations)
        nodes.append({
            "data": {"id": str(i), "label": name, "name": name, "age": age, "occupation": occupation},
            "position": random_position()
        })
    edges = []
    edge_types = ["friend", "close_friend", "work_colleagues", "family", "acquaintance"]
    possible_edges = [(str(a), str(b)) for a in range(1, num_nodes + 1) for b in range(a + 1, num_nodes + 1)]
    num_edges = random.randint(0, min(len(possible_edges), num_nodes * 2))
    selected_edges = random.sample(possible_edges, num_edges)
    for source, target in selected_edges:
        edge_type = random.choice(edge_types)
        edges.append({"data": {"source": source, "target": target, "type": edge_type}})
    return nodes + edges

@app.callback(
    Output("graph", "elements"),
    Output("info", "children"),
    Output("selected-node", "data"),
    Input("btn-generate", "n_clicks"),
    State("num-nodes", "value"),
    prevent_initial_call=True
)
def generate_nodes(n_clicks, num):
    if not num or int(num) < 1:
        return dash.no_update, "Please enter a positive integer.", dash.no_update
    num = int(num)
    nodes = initial_position(num)
    return nodes, f"{num} nodes created.", None

@app.callback(
    Output("graph", "elements", allow_duplicate=True),
    Output("info", "children", allow_duplicate=True),
    Output("selected-node", "data", allow_duplicate=True),
    Input("btn-random", "n_clicks"),
    prevent_initial_call=True
)
def generate_random(n_clicks):
    elements = generate_random_graph()
    num_nodes = len([el for el in elements if "source" not in el["data"]])
    num_edges = len([el for el in elements if "source" in el["data"]])
    return elements, f"Random graph generated with {num_nodes} nodes and {num_edges} edges.", None

@app.callback(
    Output("node-modal", "style"),
    Output("adding-new", "data"),
    Output("name-input", "value"),
    Output("age-input", "value"),
    Output("occupation-input", "value"),
    Input("btn-add-node", "n_clicks"),
    prevent_initial_call=True
)
def open_add_modal(n_clicks):
    return {"display": "block"}, True, "", "", ""

@app.callback(
    Output("tooltip", "children"),
    Input("graph", "mouseoverNodeData"),
    prevent_initial_call=True
)
def show_tooltip(mouseover_data):
    if mouseover_data:
        node_data = mouseover_data
        name = node_data.get("name", "N/A")
        age = node_data.get("age", "N/A")
        occupation = node_data.get("occupation", "N/A")
        return [f"Name: {name}", html.Br(), f"Age: {age}", html.Br(), f"Occupation: {occupation}"]
    return "Hover over a node to see details."

@app.callback(
    Output("graph", "elements", allow_duplicate=True),
    Output("info", "children", allow_duplicate=True),
    Output("selected-node", "data", allow_duplicate=True),
    Output("node-modal", "style", allow_duplicate=True),
    Input("graph", "tapNodeData"),
    State("graph", "elements"),
    State("selected-node", "data"),
    State("mode-toggle", "value"),
    State("edge-type", "value"),
    State("node-modal", "style"),
    prevent_initial_call=True
)
def handle_node_tap(tap_data, elements, selected, mode, edge_type, modal_style):
    if not tap_data:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    node_id = tap_data["id"]
    if mode == "connect":
        # Connect mode logic
        if selected is None:
            # Select the node
            for el in elements:
                if el.get("data", {}).get("id") == node_id:
                    el["classes"] = "selected"
                elif "classes" in el and "selected" in el["classes"]:
                    el["classes"] = ""
            return elements, f"Selected node {node_id}. Click another to connect.", node_id, modal_style
        elif selected == node_id:
            # Deselect if same node
            for el in elements:
                if el.get("data", {}).get("id") == node_id and "classes" in el:
                    el["classes"] = ""
            return elements, f"Deselected node {node_id}.", None, modal_style
        else:
            # Connect to selected node with selected type
            existing_edges = [el for el in elements if el.get("data", {}).get("source") and el["data"]["target"]]
            if any((el["data"]["source"] == selected and el["data"]["target"] == node_id and el["data"].get("type") == edge_type) or
                   (el["data"]["source"] == node_id and el["data"]["target"] == selected and el["data"].get("type") == edge_type) for el in existing_edges):
                return elements, f"Edge of type '{edge_type}' between {selected} and {node_id} already exists.", selected, modal_style
            # Add edge with type
            elements.append({"data": {"source": selected, "target": node_id, "type": edge_type}})
            # Deselect
            for el in elements:
                if "classes" in el and "selected" in el["classes"]:
                    el["classes"] = ""
            return elements, f"Connected {selected} to {node_id} as '{edge_type}'.", None, modal_style
    elif mode == "data":
        # Data mode: show modal for the node
        return elements, f"Editing data for node {node_id}.", None, {"display": "block"}

@app.callback(
    Output("node-modal", "style", allow_duplicate=True),
    Output("graph", "elements", allow_duplicate=True),
    Output("info", "children", allow_duplicate=True),
    Output("adding-new", "data", allow_duplicate=True),
    Input("save-btn", "n_clicks"),
    Input("cancel-btn", "n_clicks"),
    State("graph", "elements"),
    State("graph", "tapNodeData"),
    State("name-input", "value"),
    State("age-input", "value"),
    State("occupation-input", "value"),
    State("adding-new", "data"),
    prevent_initial_call=True
)
def handle_modal(save_clicks, cancel_clicks, elements, tap_data, name, age, occupation, adding_new):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "save-btn":
        if adding_new:
            # Add new node
            node_ids = []
            for el in elements:
                if "id" in el.get("data", {}):
                    id_str = el["data"]["id"]
                    if id_str.isdigit():
                        node_ids.append(int(id_str))
            max_id = max(node_ids) if node_ids else 0
            new_id = str(max_id + 1)
            new_node = {
                "data": {"id": new_id, "label": name or f"Person {new_id}", "name": name or "", "age": age or "", "occupation": occupation or ""},
                "position": random_position()
            }
            elements.append(new_node)
            return {"display": "none"}, elements, f"New node {new_id} added.", False
        else:
            # Edit existing node
            if tap_data:
                node_id = tap_data["id"]
                for el in elements:
                    if el.get("data", {}).get("id") == node_id:
                        el["data"]["name"] = name or ""
                        el["data"]["age"] = age or ""
                        el["data"]["occupation"] = occupation or ""
                        el["data"]["label"] = name or f"Person {node_id}"
                        break
                return {"display": "none"}, elements, f"Data saved for node {node_id}.", False
    return {"display": "none"}, elements, "Cancelled.", False

if __name__ == "__main__":
    app.run(debug=True)