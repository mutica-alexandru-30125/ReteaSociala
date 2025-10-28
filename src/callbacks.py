from dash import Input, Output, State, html
from utils import initial_position, random_position, generate_random_graph
import networkx as nx
from community import best_partition

def register_callbacks(app):
    @app.callback(
        Output("btn-add-node", "disabled"),
        Input("graph", "elements")
    )
    def disable_buttons(elements):
        disabled = len(elements) == 0
        return disabled
    
    @app.callback(
        Output("btn-analyse", "disabled"),
        Input("graph", "elements")
    )
    
    def disable_analyse_button(elements):
        disabled = len(elements) == 0
        return disabled

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
            return [], "Please enter a positive integer.", None
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
        Output("edge-type", "data"),
        Input("edge-type-radio", "value"),
        prevent_initial_call=True
    )
    def update_edge_type(value):
        return value

    @app.callback(
        Output("analysis", "children"),
        Input("btn-analyse", "n_clicks"),
        State("graph", "elements"),
        prevent_initial_call=True
    )
    def analyse_graph(n_clicks, elements):
        # Build NetworkX graph
        G = nx.Graph()
        for el in elements:
            if "source" not in el["data"]:
                G.add_node(el["data"]["id"], **el["data"])
            else:
                G.add_edge(el["data"]["source"], el["data"]["target"])
    
        # Compute metrics
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        deg_cent = nx.degree_centrality(G)
        clustering = nx.clustering(G)
        partition = best_partition(G)
    
        # Format the results
        results = f"Number of persons: {num_nodes}\nNumber of relations: {num_edges}\n\nDegree Centrality:\n"
        for node, cent in sorted(deg_cent.items(), key=lambda x: x[1], reverse=True):
            results += f"Node {node}: {cent:.3f}\n"
        results += "\nClustering Coefficient:\n"
        for node, clust in sorted(clustering.items(), key=lambda x: x[1], reverse=True):
            results += f"Node {node}: {clust:.3f}\n"
        results += "\nCommunities (Louvain):\n"
        communities = {}
        for node, comm in partition.items():
            if comm not in communities:
                communities[comm] = []
            communities[comm].append(node)
        for comm, nodes in communities.items():
            results += f"Community {comm}: {', '.join(nodes)}\n"
    
        return html.Pre(results)

    @app.callback(
        Output("graph", "elements", allow_duplicate=True),
        Output("info", "children", allow_duplicate=True),
        Output("selected-node", "data", allow_duplicate=True),
        Output("node-modal", "style", allow_duplicate=True),
        Input("graph", "tapNodeData"),
        State("graph", "elements"),
        State("selected-node", "data"),
        State("mode-toggle", "value"),
        State("edge-type", "data"),
        State("node-modal", "style"),
        prevent_initial_call=True
    )
    def handle_node_tap(tap_data, elements, selected, mode, edge_type, modal_style):
        if not tap_data:
            return [], [], None, modal_style
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
        elif mode == "delete":
            # Delete mode: remove the node and its edges
            elements = [el for el in elements if not (el.get("data", {}).get("id") == node_id)]
            elements = [el for el in elements if not (el.get("data", {}).get("source") == node_id or el.get("data", {}).get("target") == node_id)]
            return elements, f"Node {node_id} and its connections deleted.", None, modal_style

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
        from dash import callback_context as ctx
        if not ctx.triggered:
            return {"display": "none"}, elements, "Cancelled.", False
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