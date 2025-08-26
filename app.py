from dash import Dash, dcc, html, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State

MAPA_VAGAS = {
        "A": "A - Ampla Concorrência",
        "I": "I - Escola Renda PPI",
        "E": "E - Escola PPI",
        "J": "J - Escola Renda PPI PCD",
        "C": "C - Escola",
        "G": "G - Escola Renda",
        "H": "H - Escola Renda PCD",
        "D": "D - Escola PCD",
        "F": "F - Escola PPI PCD",
        "B": "B - PCD"
    }

MAPA_AREAS = { 
        "PEDAGOGIA": "Educação", 
        "LETRAS PORTUGUES": "Educação", 
        "LETRAS INGLES": "Educação", 
        "LETRAS - ESPANHOL": "Educação", 
        "LETRAS - PORTUGUES": "Educação", 
        "ADMINISTRAÇÃO": "Ciências Humanas e Sociais Aplicadas", 
        "GEOGRAFIA": "Ciências Humanas e Sociais Aplicadas", 
        "HISTÓRIA": "Ciências Humanas e Sociais Aplicadas", 
        "MEDICINA": "Ciências da Saúde e Biológicas", 
        "CIENCIAS BIOLOGICAS": "Ciências da Saúde e Biológicas", 
        "ENGENHARIA DE PRODUÇÃO": "Ciências Exatas e Tecnológicas", 
        "CIENCIA E TECNOLOGIA": "Ciências Exatas e Tecnológicas", 
        "ENGENHARIA DE MATERIAIS": "Ciências Exatas e Tecnológicas", 
        "GEOPROCESSAMENTO": "Ciências Exatas e Tecnológicas", 
        "FÍSICA": "Ciências Exatas e Tecnológicas", 
        "MATEMATICA": "Ciências Exatas e Tecnológicas", 
        "QUIMICA": "Ciências Exatas e Tecnológicas", 
        "AGRONOMIA": "Ciências Agrárias", 
        "ENGENHARIA FLORESTAL": "Ciências Agrárias", 
        "AGROECOLOGIA": "Ciências Agrárias",
        "ARQUITETURA E URBANISMO": "Ciências Humanas e Sociais Aplicadas",
        "ARQUIVOLOGIA": "Ciências Humanas e Sociais Aplicadas",
        "BIBLIOTECONOMIA": "Ciências Humanas e Sociais Aplicadas",
        "BIOMEDICINA": "Ciências da Saúde e Biológicas",
        "BIOTECNOLOGIA": "Ciências da Saúde e Biológicas",
        "CIÊNCIA DA COMPUTAÇÃO": "Ciências Exatas e Tecnológicas"
          }

def padronizar_curso(s: pd.Series) -> pd.Series:
    s = s.str.strip().str.upper()
    
    s = s.replace({
        "FÍSICA": "FISICA",
        "LETRAS INGLES" :"LETRAS - INGLES"
    })
    # normalização de espaços múltiplos
    s = s.str.replace(r"\s+", " ", regex=True)
    return s

# Carrega o dataset
df = pd.read_csv("data/alunos_classificados2.csv") 
df["CURSO"] = padronizar_curso(df["CURSO"])
df["VAGA CLASSIFICAÇÃO"] = df["VAGA CLASSIFICAÇÃO"].fillna("")
df["AREA"] = df["CURSO"].map(MAPA_AREAS)

def build_options(series: pd.Series):
    vals = sorted(series.dropna().unique())
    return [{"label": v, "value": v} for v in vals]

def filtrar_df(base, universidades=None, cursos=None, cidades=None, vagas=None):
    df_filtrado = base
    if universidades: df_filtrado = df_filtrado[df_filtrado["UNIVERSIDADE"].isin(universidades)]
    if cursos:        df_filtrado = df_filtrado[df_filtrado["CURSO"].isin(cursos)]
    if cidades:       df_filtrado = df_filtrado[df_filtrado["CIDADE"].isin(cidades)]
    if vagas:         df_filtrado = df_filtrado[df_filtrado["VAGA CLASSIFICAÇÃO"].isin(vagas)]
    return df_filtrado

def percent_feminino(df_):
    vc = df_["SEXO"].value_counts()
    total = vc.sum()
    fem = vc.get("F", 0)
    return (fem/total*100) if total else 0

# Inicializar o app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Aprovados"

# Layout
app.layout = dbc.Container([
    html.H1(" 📊 Aprovados em Universidades Públicas", className="text-center my-4"),

    html.Hr(),

    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.P("Mais de mil estudantes conquistaram vaga", className="kpi-title"),
                html.H2(f"{len(df)}", className="kpi-value")
            ])
        ], className="kpi-card kpi-green"), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.P("Mulheres são maioria entre os aprovados", className="kpi-title"),
                html.H2(f"{percent_feminino(df):.1f}%", className="kpi-value")
            ])
        ], className="kpi-card kpi-blue"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Quase metade dos aprovados veio por cotas", className="kpi-title"),
                html.H2(f"{(df['VAGA CLASSIFICAÇÃO'].apply(lambda x: 'A' not in x).mean()*100):.1f}%", className="kpi-value")
            ])
        ], className="kpi-card kpi-cyan"), width=3),

        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Nota Média dos alunos aprovados", className="kpi-title"),
                html.H2(f"{df['PONTUAÇÃO'].mean():.2f}", className="kpi-value")
            ])
        ], className="kpi-card kpi-teal"), width=3),
    ], className="mb-4"),

    # Filtros
    dbc.Row([
        dbc.Col([
            html.Label("Universidade"),
            dcc.Dropdown(options=build_options(df["UNIVERSIDADE"]),
                         placeholder="Selecione a universidade", multi=True, id="filtro_universidade")
        ], width=3),

        dbc.Col([
            html.Label("Campus"),
            dcc.Dropdown(options=build_options(df["CIDADE"]),
                         placeholder="Selecione a cidade", multi=True, id="filtro_cidade")
        ], width=3),

        dbc.Col([
            html.Label("Curso"),
            dcc.Dropdown(options=build_options(df["CURSO"]),
                         placeholder="Selecione o curso", multi=True, id="filtro_curso")
        ], width=3),

        dbc.Col([
            html.Label("Vaga"),
            dcc.Dropdown(options=[
                {'label': MAPA_VAGAS.get(v, v), 'value': v}
                  for v in sorted(df['VAGA CLASSIFICAÇÃO'].unique())],
                 placeholder="Selecione a modalidade de vaga", multi=True, id="filtro_vaga")
        ], width=3)
    ]),

    html.Hr(),

    # Gráficos
    dbc.Row([
        dbc.Col(
            dcc.Graph(id="grafico_vaga", config={"displayModeBar": False}),
        width=6, className="grafico-sombreado m-2"),

        dbc.Col(
            dcc.Graph(id="grafico_sexo", config={"displayModeBar": False}),
        width=5, className="grafico-sombreado m-2"),

        dbc.Col(
            dcc.Graph(id="grafico_area", config={"displayModeBar": False}),
            width=11, className="grafico-sombreado m-2"),
   
        dbc.Col(
            dcc.Graph(id="grafico_sexo_por_area", config={"displayModeBar": False}), 
            width=11, className="grafico-sombreado m-2"),      
    ])
], style={"maxWidth": "1800px", "margin": "0 auto"}),

@app.callback(
    Output("grafico_vaga", "figure"),
    [
        Input("filtro_universidade", "value"),
        Input("filtro_curso", "value"),
        Input("filtro_cidade", "value"),
        Input("filtro_vaga", "value"),
    ]
)

def grafico_vaga(universidade, curso, cidade, vaga):
    # Copia do DataFrame original
    df_filtrado = filtrar_df(df, universidade, curso, cidade, vaga).copy()
    
    df_filtrado['VAGA CLASSIFICAÇÃO'] = df_filtrado['VAGA CLASSIFICAÇÃO'].map(MAPA_VAGAS)

    contagem = df_filtrado['VAGA CLASSIFICAÇÃO'].value_counts().reset_index()
    contagem.columns = ['VAGA CLASSIFICAÇÃO', 'TOTAL']
    
    fig = px.bar(
        contagem,
        x='VAGA CLASSIFICAÇÃO',
        y='TOTAL',
        text='TOTAL',
        title='A maioria entrou por ampla concorrência, mas 42% são cotistas',
        labels={'TOTAL': 'Total de Aprovados'},
        color='VAGA CLASSIFICAÇÃO'
    )
    fig.update_layout(xaxis_title="Tipo de Vaga", 
                      yaxis_title="Total", 
                      plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)", 
                      title_x=0.5,
                      height=400)

    return fig

@app.callback(
    Output("grafico_sexo", "figure"),
    [
        Input("filtro_universidade", "value"),
        Input("filtro_curso", "value"),
        Input("filtro_cidade", "value"),
        Input("filtro_vaga", "value"),
    ]
)

def grafico_sexo(universidade, curso, cidade, vaga):
    df_filtrado = filtrar_df(df, universidade, curso, cidade, vaga).copy()

    contagem = df_filtrado['SEXO'].value_counts().reset_index()
    contagem.columns = ['SEXO', 'TOTAL']

    perc_fem = (contagem.loc[contagem["SEXO"] == "F", "TOTAL"].sum() / contagem["TOTAL"].sum() * 100) if contagem["TOTAL"].sum() else 0 
    
    contagem['SEXO'] = contagem['SEXO'].replace({
    'F': 'Feminino',
    'M': 'Masculino'})

    filtros_ativos = any([
        universidade, curso, cidade, vaga
    ])

    if not filtros_ativos:
        titulo = f"Mulheres representam a maioria dos aprovados ({perc_fem:.1f}%)"
    else:
        filtros_txt = []
        if universidade:
            filtros_txt.append(f"Universidade(s): {', '.join(universidade)}")
        if curso:
            filtros_txt.append(f"Curso(s): {', '.join(curso)}")
        if cidade:
            filtros_txt.append(f"Cidade(s): {', '.join(cidade)}")
        if vaga:
            filtros_txt.append(f"Vaga(s): {', '.join(vaga)}")

        filtros_str = " | <br>".join(filtros_txt)
        titulo = f"Distribuição por Sexo <br> <sup>(Filtros aplicados: {filtros_str})</sup>"

    fig = px.pie(
        contagem,
        names='SEXO',
        values='TOTAL',
        title=titulo,
        color="SEXO",
        color_discrete_map={
            "Feminino": "#0ea5e9",   
            "Masculino": "#ffffb3" 
        }
    )
    fig.update_traces(textinfo='percent+label')
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)",
                      paper_bgcolor="rgba(0,0,0,0)", 
                      title_x=0.5,
                      height=400)

    return fig

opcoes_curso_todas = [
    {'label': c, 'value': c}
    for c in sorted(df['CURSO'].dropna().unique())
]

@app.callback(
    Output("filtro_curso", "options"),
    Output("filtro_curso", "value"),
    Input("filtro_cidade", "value"),
    State("filtro_curso", "value"),  # para preservar o que já estava selecionado
)
def atualizar_cursos_por_cidade(cidades_selecionadas, cursos_selecionados):
    # sem filtros
    if not cidades_selecionadas:
        return opcoes_curso_todas, no_update

    # filtro pelas cidades escolhidas
    df_subset = df[df["CIDADE"].isin(cidades_selecionadas)]

    # opcoes validas por cidade
    cursos_validos = sorted(df_subset["CURSO"].dropna().unique())
    options = [{'label': c, 'value': c} for c in cursos_validos]

    if cursos_selecionados:
       
        if isinstance(cursos_selecionados, str):
            cursos_selecionados = [cursos_selecionados]
        novos_values = [c for c in cursos_selecionados if c in cursos_validos]
    else:
        novos_values = []

    return options, novos_values

@app.callback(
    Output("grafico_area", "figure"),
    [
        Input("filtro_universidade", "value"),
        Input("filtro_curso", "value"),
        Input("filtro_cidade", "value"),
        Input("filtro_vaga", "value"),
    ]
)

def grafico_area(universidade, curso, cidade, vaga):
    # Copia do DataFrame original
    df_filtrado = filtrar_df(df, universidade, curso, cidade, vaga).copy()

    df_filtrado['AREA'] = df_filtrado['CURSO'].map(MAPA_AREAS)

    contagem = (
        df_filtrado['AREA']
        .value_counts()
        .reset_index()
        .rename(columns={'index': 'AREA', 'AREA': 'TOTAL'})
        .sort_values('TOTAL', ascending=False)
        .reset_index(drop=True)
    )

    contagem.columns = ['AREA', 'TOTAL']

    # Se não houver dados após filtros
    if contagem.empty:
        fig = px.bar(title="Sem dados para os filtros aplicados")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", 
                          paper_bgcolor="rgba(0,0,0,0)", 
                          title_x=0.5, 
                          height=500)
        return fig
    
    # Área com maior aquisição
    idx_max = contagem["TOTAL"].idxmax()
    top_area = contagem.loc[idx_max, 'AREA']
    top_total = int(contagem.loc[idx_max, 'TOTAL'])
    total_geral = int(contagem['TOTAL'].sum())
    top_share = (top_total / total_geral * 100) if total_geral > 0 else 0

    # título dinâmico
    filtros = []
    if universidade: filtros.append(f"Universidade(s): {', '.join(universidade)}")
    if cidade:       filtros.append(f"Cidade(s): {', '.join(cidade)}")
    if vaga:         filtros.append(f"Vaga(s): {', '.join(vaga)}")
    subtitulo = f"<br><sup>Filtros: {' | '.join(filtros)}</sup>" if filtros else ""

    titulo = f"{top_area} é a área com maior aquisição ({top_total} alunos, {top_share:.1f}%)" + subtitulo

    ordem = contagem['AREA'].tolist()
    cores = ['#17becf' if a == top_area else '#cbd5e1' for a in ordem]

    # Gráfico
    fig = px.bar(
        contagem,
        x='AREA',
        y='TOTAL',
        text='TOTAL',
        title=titulo)
  
    fig.update_xaxes(categoryorder='array', categoryarray=ordem)
    fig.update_traces(marker_color=cores, selector=dict(type='bar'), textposition='outside', showlegend=False, cliponaxis=False)
    
    fig.update_layout(
        xaxis_title="Área",
        yaxis_title="Total",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        title_x=0.5,
        height=400 
    )

    return fig

@app.callback(
    Output("grafico_sexo_por_area", "figure"),
    [
        Input("filtro_universidade", "value"),
        Input("filtro_curso", "value"),
        Input("filtro_cidade", "value"),
        Input("filtro_vaga", "value"),
    ]
)

def grafico_sexo_por_area(universidade, curso, cidade, vaga):
    df_filtrado = filtrar_df(df, universidade, curso, cidade, vaga).copy()
    df_filtrado["AREA"] = df_filtrado["CURSO"].map(MAPA_AREAS)

    # agrega sexo por área
    contagem_sexo_area = (
        df_filtrado
        .groupby(["AREA", "SEXO"])
        .size()
        .reset_index(name="TOTAL")
        .dropna(subset=["AREA"])
    )

    contagem_sexo_area["SEXO"] = contagem_sexo_area["SEXO"].replace(
        {"F": "Feminino", "M": "Masculino"}
    )

    contagem_sexo_area["PERC"] = contagem_sexo_area.groupby("AREA")["TOTAL"].transform(
        lambda x: x / x.sum() * 100
    )

    # conta qual area mais dominante por sexo
    area_fem = (contagem_sexo_area[contagem_sexo_area["SEXO"] == "Feminino"]
                .sort_values("PERC", ascending=False)
                .head(1))
    area_masc = (contagem_sexo_area[contagem_sexo_area["SEXO"] == "Masculino"]
                 .sort_values("PERC", ascending=False)
                 .head(1))

    if not area_fem.empty and not area_masc.empty:
        titulo = (f"Mulheres dominan em {area_fem.iloc[0]['AREA']} "
                  f"({area_fem.iloc[0]['PERC']:.1f}%) e "
                  f"Homens em {area_masc.iloc[0]['AREA']} "
                  f"({area_masc.iloc[0]['PERC']:.1f}%)")
    else:
        titulo = "Distribuição por Sexo em cada Área"
    
    fig = px.pie(
        contagem_sexo_area,
        names="SEXO",
        values="TOTAL",
        color="SEXO",
        color_discrete_map={"Feminino": "#0ea5e9", "Masculino": "#ffffb3"},
        facet_col="AREA",  
        hole=0.55,
        title=titulo
    )

    fig.update_traces(textinfo="percent", textposition="inside", showlegend=True)
    fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))  # mostra só o nome da área

    fig.update_layout(
        legend_title_text="Sexo",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        title_x=0.5,
        yaxis=dict(       
        categoryorder="total ascending"  # ordena pelas quantidades 
        ),
    )
    return fig

# Rodar o servidor
if __name__ == "__main__":
    app.run(debug=True)
