# 📊 Dashboard de Aprovados em Universidades Públicas

Este projeto tem como objetivo explorar dados reais de estudantes aprovados em universidades públicas brasileiras por meio de um dashboard interativo. Desenvolvido com [Dash](https://dash.plotly.com/) e [Plotly](https://plotly.com/python/), o sistema permite filtrar dados por curso, campus, tipo de vaga, sexo, entre outros.

## ✨ Funcionalidades

- Visualização de KPIs: total de aprovados, nota média, % de cotistas e % de mulheres.
- Gráficos dinâmicos:

  - Barras por tipo de vaga
  - Pizza por distribuição de sexo
  - Barras por área
  - Pizza por distribuição de sexo por área

- Filtros por curso, campus e modalidade de ingresso

## 🚀 Tecnologias utilizadas

- Python
- Dash
- Plotly
- Pandas

---

## ✅ Requisitos

- **Python 3.10+** (recomendado)
- **pip** atualizado
- (Opcional) **Git** instalado para clonar o repositório

---

## 🚀 Como rodar o projeto localmente

### 1) Clone o repositório

```bash
git clone https://github.com/SamillyBeatriz/aprovados_dashboard.git
cd aprovados_dashboard
```

### 2) Crie e ative um ambiente virtual

- Windows (PowerShell):

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

- macOS/ Linux:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3) Instale as dependências

```bash
pip install -r requirements.txt

```

### 4) Garanta o dataset no caminho esperado

- O app lê o CSV em data/alunos_classificados2.csv.
  Certifique-se de que esse arquivo está disponível nesse diretório.

### 5) Execute o aplicativo

- Rode o servidor local:

```bash
python app.py
```

O app ficará disponível em:
👉 http://127.0.0.1:8050

## 📊 Fonte dos Dados

Os dados utilizados neste projeto foram obtidos no site oficial do **CEPS/UFPA**:  
👉 [Resultado Final PS 2024 – CEPS/UFPA](https://www.ceps.ufpa.br/index.php/ps2024/742-resultados-ps2024/1711-resultado-final-ps2024)

---

### 📝 Licença

Este projeto é de caráter educacional e demonstrativo.
Sinta-se à vontade para adaptar e expandir.

---
