import pickle

with open('pickle/final_files','rb') as file:
    final_files = pickle.load(file)

with open('pickle/y_tsne','rb') as file:
    y_tsne = pickle.load(file)

with open('pickle/y_umap','rb') as file:
    y_umap = pickle.load(file)

with open('pickle/pca_remapped_colors','rb') as file:
    pca_remapped_colors = pickle.load(file)

with open('pickle/tsne_remapped_colors','rb') as file:
    tsne_remapped_colors = pickle.load(file)

with open('pickle/umap_remapped_colors','rb') as file:
    umap_remapped_colors = pickle.load(file)

#===============================================
import plotly.graph_objs as go
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot


# init_notebook_mode(connected=True)

y_graph = y_tsne

def file_readin(filename):
    with open (f'bbc/all/{filename}', 'r') as file:
        text = file.read()
    text = str(text).replace('.','.<br>').replace('\n','<br>')

    return text

#dash file return
def dash_file_readin(filename):
    with open (f'bbc/all/{filename}', 'r') as file:
        text = file.read()
    text = text.split('\n')
#     text = str(text).replace('.','.<br>').replace('\n','<br>')

    return text

color_lookup = {'b':'blue', 'e':'red', 'p':'yellow','s':'pink','t':'green'}
def color_mapping(i, view_style):
    if view_style == 'pca':
        color = pca_remapped_colors[i]
    if view_style == 'tsne':
        color = tsne_remapped_colors[i]
    if view_style == 'umap':
        color = umap_remapped_colors[i]
    r = color[0]
    g = color[1]
    b = color[2]
    color = f'rgb({r},{g},{b})'
    return color

data = [
    go.Scatter(
        x=[i[0] for i in y_graph],
        y=[i[1] for i in y_graph],
        mode='markers',
        hoverinfo='text',
#         text=[file_readin(i) for i in final_files],
        text=[i for i in final_files],
        showlegend=False,
    marker=dict(
        size=8,
        color = [color_lookup[i[0]]for i in final_files], #set color equal to a variable
#         color = [color_mapping(i) for i in range(len(final_files))], #set color equal to a variable
#         color = 'rgb(10,50,10)',
        opacity= 0.8,
        colorscale='Viridis',
        showscale=False,
    )
    )
]
def get_color_set(num):
    if num == 1:
        marker_color = [color_lookup[i[0]]for i in final_files]
    if num == 2:
        marker_color = [color_mapping(i,'tsne') for i in range(len(final_files))]
    if num == 3:
        marker_color = [color_mapping(i,'pca') for i in range(len(final_files))]
    if num == 4:
        marker_color = [color_mapping(i,'umap') for i in range(len(final_files))]
    return [{'marker.color': [marker_color]}]

updatemenus = list([
            dict(
                buttons=list([
                    dict(label = 'Color by Document Label',
                         method = 'update',
                         args=get_color_set(1)
                    ),
                    dict(label = 'Color by PCA(50)>>T-SNE(3)',
                         method = 'update',
                         args=get_color_set(2)
                    ),
                    dict(label = 'Color by PCA(3)',
                         method = 'update',
                         args=get_color_set(3)
                    ),
                    dict(label = 'Color by UMAP(3) neighbors = 5',
                         method = 'update',
                         args=get_color_set(4)
                    ),

                ]),
                direction = 'left',
                pad = {'r': 10, 't': 10},
                showactive = False,
                type = 'buttons',
                x = 0.1,
                xanchor = 'left',
                y = 1.1,
                yanchor = 'top'
            )
        ])
layout = go.Layout()
layout = dict(hovermode = 'closest',
#               hoverlabel_align = 'right',
              hoverlabel_font_size = 10,
              yaxis = dict(zeroline = False, showgrid=False, showticklabels=False),
              xaxis = dict(zeroline = False, showgrid=False, showticklabels=False),
              template = 'plotly_dark',
              paper_bgcolor = '#0d112b',
              plot_bgcolor = '#0d112b',
              updatemenus = updatemenus,
             )
fig = go.Figure(data=data, layout=layout)
# file = plot(fig, filename='Sentence_encode.html')
#=====================================================================
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.css.append_css({'external_url': '/assets/style.css'})
server = app.server 

colors = {
    'text':'#ff0000',
    'plot_color':'#D3D3D3',
    'paper_color':'#00FFFF',
    'background':'#000000'
}

app.layout = html.Div(id='wrapper', style={'display':'grid','grid-template-columns':'2fr 1fr', 'background-color':'#0d112b'},children = [
    html.Div(dcc.Graph(
            id='scatterChart',
            style={'height':'100vh'},
            figure = fig,
            config={
                'displayModeBar': False
            }
        )),
    html.Div(id='fullText',
             style={'background': 'linear-gradient(to left, #111111 0%, #0d112b 95%)', 'padding':'15px 30px'},
             children = [html.P(id='output16', style={'color':'white', 'font-family':'Merriweather','font-weight':'bold', 'font-size':'2em'}),
                        html.P(id='output17', style={'color':'white', 'font-family':'Merriweather','font-weight':'bold','font-size':'1em','font-style':'italic'}),
                        html.P(id='output18', style={'color':'white', 'text-align':'justify', 'font-family':'Merriweather'})])

    ])

@app.callback([
    Output(component_id='output16', component_property='children'),
    Output(component_id='output17', component_property='children'),
    Output(component_id='output18', component_property='children')],
    [Input(component_id='scatterChart', component_property='hoverData')]
)
def multi_output(input_data):
    input_data = input_data['points'][0]['text']
    text = dash_file_readin(input_data)
#     text = text[0]+'\n'+text[1]+'\n'+text[2:]
    title = text[0]
    heading = text[2]
    body = ' '.join(text[3:])
    return title, heading, body

if __name__ == '__main__':
    app.run_server()
