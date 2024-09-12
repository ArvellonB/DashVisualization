import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import io
import base64

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Dynamic Data Dashboard'),

    # File upload component
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV'),
        multiple=False
    ),
    html.Div(id='output-data-upload'),

    # Graph component
    dcc.Graph(id='line-plot')
])

# Callback to process uploaded file and generate plot
@app.callback(
    Output('output-data-upload', 'children'),
    Output('line-plot', 'figure'),
    Input('upload-data', 'contents')
)
def update_output(contents):
    if contents is None:
        return 'Upload a CSV file to see the data.', {}

    # Decode the file content
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    # Check if the DataFrame is valid
    if df.empty:
        return 'File is empty or invalid CSV.', {}

    # Create a Plotly figure
    fig = px.line(df, x=df.columns[0], y=df.columns[1], title='Uploaded Data Visualization')

    return 'File uploaded successfully.', fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
