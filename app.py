from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

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

    # Placeholder
    html.Div("Gráficos serão inseridos aqui.", id="graficos_placeholder", className="text-muted text-center mt-4")
], fluid=True)

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=True)
