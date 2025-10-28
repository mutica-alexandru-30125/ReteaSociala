import dash
import dash_cytoscape as cyto
from layout import create_layout
from callbacks import register_callbacks

app = dash.Dash(__name__)

app.layout = create_layout()

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)