import dash
import dash_bootstrap_components as dbc
from layout import layout
from callbacks import register_callbacks

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the layout
app.layout = layout

# Register callbacks
register_callbacks(app)

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)

