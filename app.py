from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Carrega o dataset
df = pd.read_csv("data/alunos_classificados.csv") 

# Inicializar o app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Aprovados"

# Layout
app.layout = dbc.Container([
    html.H1("Dashboard de Aprovados em Universidades Públicas", className="text-center my-4"),

    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total de Aprovados", className="card-title"),
                html.H2(f"{len(df)}", className="card-text")
            ])
        ], color="primary", inverse=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Nota Média", className="card-title"),
                html.H2(f"{df['PONTUACAO'].mean():.2f}", className="card-text")
            ])
        ], color="success", inverse=True), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Percentual Mulheres", className="card-title"),
                html.H2(f"{(df['SEXO'].value_counts(normalize=True).get('F', 0)*100):.1f}%", className="card-text")
            ])
        ], color="info", inverse=True), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Percentual Cotistas", className="card-title"),
                html.H2(f"{(df['VAGA CLASSIFICACAO'].apply(lambda x: 'AC' not in x).mean()*100):.1f}%", className="card-text")
            ])
        ], color="warning", inverse=True), width=3)
    ], className="mb-4"),

    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Curso"),
            dcc.Dropdown(options=[{'label': c, 'value': c} for c in sorted(df['CURSO'].unique())],
                         placeholder="Selecione o curso", multi=True, id="filtro_curso")
        ], width=4),

        dbc.Col([
            html.Label("Campus"),
            dcc.Dropdown(options=[{'label': c, 'value': c} for c in sorted(df['CAMPUS'].unique())],
                         placeholder="Selecione o campus", multi=True, id="filtro_campus")
        ], width=4),

        dbc.Col([
            html.Label("Vaga"),
            dcc.Dropdown(options=[{'label': v, 'value': v} for v in sorted(df['VAGA CLASSIFICACAO'].unique())],
                         placeholder="Selecione a modalidade de vaga", multi=True, id="filtro_vaga")
        ], width=4)
    ]),

    html.Hr(),
dbc.Row([
    dbc.Col(
    dcc.Graph(id="grafico_vaga", config={"displayModeBar": False}),
    width=6),
    dbc.Col(
    dcc.Graph(id="grafico_sexo", config={"displayModeBar": False}),
    width=6
    )
])
], fluid=True)

@app.callback(
    Output("grafico_vaga", "figure"),
    [
        Input("filtro_curso", "value"),
        Input("filtro_campus", "value"),
        Input("filtro_vaga", "value"),
    ]
)

def atualizar_grafico_vaga(curso, campus, vaga):
    # Copia do DataFrame original
    df_filtrado = df.copy()

    # Aplicar filtros se selecionados
    if curso:
        df_filtrado = df_filtrado[df_filtrado['CURSO'].isin(curso)]
    if campus:
        df_filtrado = df_filtrado[df_filtrado['CAMPUS'].isin(campus)]
    if vaga:
        df_filtrado = df_filtrado[df_filtrado['VAGA CLASSIFICACAO'].isin(vaga)]

    # Agrupar dados para o gráfico
    contagem = df_filtrado['VAGA CLASSIFICACAO'].value_counts().reset_index()
    contagem.columns = ['VAGA CLASSIFICACAO', 'TOTAL']

    # Criar gráfico de barras com Plotly
    fig = px.bar(
        contagem,
        x='VAGA CLASSIFICACAO',
        y='TOTAL',
        text='TOTAL',
        title='Número de Aprovados por Tipo de Vaga',
        labels={'TOTAL': 'Total de Aprovados'},
        color='VAGA CLASSIFICACAO'
    )
    fig.update_layout(xaxis_title="Tipo de Vaga", yaxis_title="Total", title_x=0.5)

    return fig

@app.callback(
    Output("grafico_sexo", "figure"),
    [
        Input("filtro_curso", "value"),
        Input("filtro_campus", "value"),
        Input("filtro_vaga", "value"),
    ]
)

def atualizar_grafico_sexo(curso, campus, vaga):
    df_filtrado = df.copy()

    if curso:
        df_filtrado = df_filtrado[df_filtrado['CURSO'].isin(curso)]
    if campus:
        df_filtrado = df_filtrado[df_filtrado['CAMPUS'].isin(campus)]
    if vaga:
        df_filtrado = df_filtrado[df_filtrado['VAGA CLASSIFICACAO'].isin(vaga)]

    contagem = df_filtrado['SEXO'].value_counts().reset_index()
    contagem.columns = ['SEXO', 'TOTAL']

    fig = px.pie(
        contagem,
        names='SEXO',
        values='TOTAL',
        title='Distribuição por Sexo',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(title_x=0.5)

    return fig


# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=True)
