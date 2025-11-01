"""
Dashboard Completo V2 - Sem iframes
Incorpora os gráficos diretamente no HTML para evitar problemas de CORS
"""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from datetime import datetime
import plotly.express as px
from scipy import stats
import numpy as np


def criar_todos_graficos(df):
    """Cria todos os gráficos e retorna como HTML"""
    
    graficos = {}
    
    # ========== CARACTERIZAÇÃO ==========
    
    # 1. Distribuição de linguagens
    lang_counts = df['linguagem'].value_counts().reset_index()
    lang_counts.columns = ['Linguagem', 'Quantidade']
    fig = px.bar(lang_counts, x='Linguagem', y='Quantidade',
                 title='Distribuição de Repositórios por Linguagem de Programação',
                 color='Quantidade', color_continuous_scale='Viridis', text='Quantidade')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(xaxis_title='Linguagem de Programação', yaxis_title='Número de Repositórios',
                     showlegend=False, height=500)
    graficos['viz1'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # 2. Métricas de popularidade
    metricas = df.groupby('linguagem').agg({'stars': 'median', 'forks': 'median', 'contributors': 'median'}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Stars', x=metricas['linguagem'], y=metricas['stars'], marker_color='gold'))
    fig.add_trace(go.Bar(name='Forks', x=metricas['linguagem'], y=metricas['forks'], marker_color='lightblue'))
    fig.add_trace(go.Bar(name='Contributors', x=metricas['linguagem'], y=metricas['contributors'], marker_color='lightgreen'))
    fig.update_layout(title='Métricas de Popularidade por Linguagem (Mediana)', barmode='group', height=500)
    graficos['viz2'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # 3. Distribuição de stars
    fig = px.box(df, x='linguagem', y='stars', title='Distribuição de Stars por Linguagem',
                color='linguagem', log_y=True)
    fig.update_layout(showlegend=False, height=500)
    graficos['viz3'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # 4. Timeline
    df_temp = df.copy()
    df_temp['ano_mes'] = pd.to_datetime(df['created_at']).dt.to_period('M')
    timeline = df_temp.groupby(['ano_mes', 'linguagem']).size().reset_index(name='quantidade')
    timeline['ano_mes'] = timeline['ano_mes'].astype(str)
    fig = px.line(timeline, x='ano_mes', y='quantidade', color='linguagem',
                 title='Timeline de Criação de Repositórios por Linguagem', markers=True)
    fig.update_layout(height=500, xaxis={'tickangle': -45})
    graficos['viz4'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # 5. Atividade
    fig = px.scatter(df, x='idade_dias', y='commits', color='linguagem', size='contributors',
                    hover_data=['repositorio', 'stars'], title='Atividade dos Repositórios: Commits vs Idade',
                    log_y=True)
    fig.update_layout(height=600)
    graficos['viz5'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # 6. Licenças
    licencas = df['licenca'].value_counts().reset_index()
    licencas.columns = ['Licença', 'Quantidade']
    fig = px.pie(licencas, values='Quantidade', names='Licença',
                title='Distribuição de Licenças nos Repositórios', hole=0.3)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=500)
    graficos['viz6'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # 7. Categorias
    categorias = df['categoria'].value_counts().reset_index()
    categorias.columns = ['Categoria', 'Quantidade']
    fig = px.bar(categorias, x='Quantidade', y='Categoria', orientation='h',
                title='Distribuição de Repositórios por Categoria', color='Quantidade',
                color_continuous_scale='Blues', text='Quantidade')
    fig.update_traces(texttemplate='%{text}', textposition='outside')
    fig.update_layout(showlegend=False, height=500)
    graficos['viz7'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # ========== RQs ==========
    
    # RQ1.1: Stars vs Commits
    fig = px.scatter(df, x='commits', y='stars', color='linguagem', size='contributors',
                    hover_data=['repositorio'], title='RQ1.1: Relação entre Stars e Commits',
                    log_x=True, log_y=True)
    fig.update_layout(height=600)
    graficos['rq1'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ1.2: Stars vs Contributors
    fig = px.scatter(df, x='contributors', y='stars', color='linguagem', size='commits',
                    hover_data=['repositorio'], title='RQ1.2: Relação entre Stars e Contributors',
                    log_x=True, log_y=True)
    fig.update_layout(height=600)
    graficos['rq2'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ1.3: Matriz de correlação
    metricas_correlacao = ['stars', 'forks', 'commits', 'contributors', 'pull_requests']
    corr_matrix = df[metricas_correlacao].corr()
    fig = go.Figure(data=go.Heatmap(z=corr_matrix.values, x=metricas_correlacao, y=metricas_correlacao,
                                    colorscale='RdBu', zmid=0, text=corr_matrix.values.round(2),
                                    texttemplate='%{text}', textfont={"size": 12}))
    fig.update_layout(title='RQ1.3: Matriz de Correlação', height=600, width=700)
    graficos['rq3'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ2.1: Taxa de resolução (box)
    fig = px.box(df, x='linguagem', y='taxa_resolucao_issues', color='linguagem',
                title='RQ2.1: Taxa de Resolução de Issues por Linguagem', points='outliers')
    fig.update_layout(showlegend=False, height=600)
    graficos['rq4'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ2.2: Taxa de resolução (violin)
    fig = px.violin(df, x='linguagem', y='taxa_resolucao_issues', color='linguagem', box=True,
                   title='RQ2.2: Distribuição da Taxa de Resolução de Issues', points='all')
    fig.update_layout(showlegend=False, height=600)
    graficos['rq5'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ2.3: Taxa média
    media = df.groupby('linguagem')['taxa_resolucao_issues'].agg(['mean', 'std']).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(x=media['linguagem'], y=media['mean'],
                        error_y=dict(type='data', array=media['std']),
                        marker_color='steelblue', text=media['mean'].round(1),
                        texttemplate='%{text}%', textposition='outside'))
    fig.update_layout(title='RQ2.3: Taxa Média de Resolução de Issues', height=600)
    graficos['rq6'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ3
    df_temp = df.copy()
    df_temp['nivel_documentacao'] = 'Nenhuma'
    df_temp.loc[df_temp['tem_readme'] == True, 'nivel_documentacao'] = 'README'
    df_temp.loc[(df_temp['tem_readme'] == True) & (df_temp['tem_wiki'] == True), 'nivel_documentacao'] = 'README + Wiki'
    
    # RQ3.1: Comparação de métricas
    fig = make_subplots(rows=2, cols=2, subplot_titles=('Stars', 'Forks', 'Contributors', 'Pull Requests'))
    colors = {'Nenhuma': 'red', 'README': 'orange', 'README + Wiki': 'green'}
    metricas = ['stars', 'forks', 'contributors', 'pull_requests']
    for idx, metrica in enumerate(metricas):
        row = idx // 2 + 1
        col = idx % 2 + 1
        dados = df_temp.groupby('nivel_documentacao')[metrica].median().reset_index()
        fig.add_trace(go.Bar(x=dados['nivel_documentacao'], y=dados[metrica],
                            marker_color=[colors[x] for x in dados['nivel_documentacao']],
                            showlegend=False), row=row, col=col)
    fig.update_layout(title_text='RQ3.1: Métricas de Engajamento por Nível de Documentação', height=800)
    graficos['rq7'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ3.2: Box plot
    fig = px.box(df_temp, x='nivel_documentacao', y='stars', color='nivel_documentacao',
                title='RQ3.2: Distribuição de Stars por Nível de Documentação', log_y=True,
                color_discrete_map=colors)
    fig.update_layout(showlegend=False, height=600)
    graficos['rq8'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ4.1: Métricas por licença
    medianas = df.groupby('licenca').agg({'stars': 'median', 'forks': 'median', 'contributors': 'median'}).reset_index()
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Stars', x=medianas['licenca'], y=medianas['stars'], marker_color='gold'))
    fig.add_trace(go.Bar(name='Forks', x=medianas['licenca'], y=medianas['forks'], marker_color='lightblue'))
    fig.add_trace(go.Bar(name='Contributors', x=medianas['licenca'], y=medianas['contributors'], marker_color='lightgreen'))
    fig.update_layout(title='RQ4.1: Métricas por Tipo de Licença (Mediana)', barmode='group', height=600)
    graficos['rq9'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ4.2: Violin plot
    fig = px.violin(df, x='licenca', y='stars', color='licenca', box=True,
                   title='RQ4.2: Distribuição de Stars por Tipo de Licença', log_y=True, points='outliers')
    fig.update_layout(showlegend=False, height=600)
    graficos['rq10'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    # RQ4.3: Scatter
    fig = px.scatter(df, x='stars', y='contributors', color='licenca', size='forks',
                    hover_data=['repositorio'], title='RQ4.3: Popularidade vs Contribuição por Tipo de Licença',
                    log_x=True, log_y=True)
    fig.update_layout(height=600)
    graficos['rq11'] = fig.to_html(full_html=False, include_plotlyjs=False)
    
    return graficos


def gerar_dashboard_sem_iframes(df):
    """Gera dashboard completo sem usar iframes"""
    
    print("\n[INFO] Gerando dashboard sem iframes (solucao para problemas de CORS)...")
    
    graficos = criar_todos_graficos(df)
    
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Lab 04 - Análise de Repositórios GitHub</title>
    <script src="https://cdn.plot.ly/plotly-2.27.0.min.js" charset="utf-8"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(to bottom, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .visualization {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .visualization h3 {{
            color: #667eea;
            margin-top: 0;
            border-bottom: 2px solid #e9ecef;
            padding-bottom: 10px;
        }}
        .section-title {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .section-title h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin: 0;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }}
        .rq-box {{
            background: #f8f9fa;
            padding: 20px;
            border-left: 4px solid #764ba2;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .rq-box h3 {{
            color: #764ba2;
            margin: 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Dashboard de Análise de Repositórios GitHub</h1>
            <p style="font-size: 1.2em; margin: 10px 0;">Laboratório 04 - Visualização de Dados com Business Intelligence</p>
            <p>Análise de {len(df)} repositórios | {df['linguagem'].nunique()} linguagens | Período: {df['created_at'].min()} a {df['created_at'].max()}</p>
        </div>

        <div class="section-title">
            <h2>📈 Parte 1: Caracterização do Dataset</h2>
            <p>Esta seção apresenta as características principais do dataset utilizado.</p>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{len(df)}</div>
                    <div>Repositórios</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{df['linguagem'].nunique()}</div>
                    <div>Linguagens</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{df['stars'].median():.0f}</div>
                    <div>Stars (mediana)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{df['contributors'].median():.0f}</div>
                    <div>Contributors (mediana)</div>
                </div>
            </div>
        </div>

        <div class="visualization"><h3>1. Distribuição de Repositórios por Linguagem</h3>{graficos['viz1']}</div>
        <div class="visualization"><h3>2. Métricas de Popularidade por Linguagem</h3>{graficos['viz2']}</div>
        <div class="visualization"><h3>3. Distribuição de Stars por Linguagem</h3>{graficos['viz3']}</div>
        <div class="visualization"><h3>4. Timeline de Criação de Repositórios</h3>{graficos['viz4']}</div>
        <div class="visualization"><h3>5. Atividade dos Repositórios</h3>{graficos['viz5']}</div>
        <div class="visualization"><h3>6. Distribuição de Licenças</h3>{graficos['viz6']}</div>
        <div class="visualization"><h3>7. Distribuição por Categoria</h3>{graficos['viz7']}</div>

        <div class="section-title">
            <h2>🔬 Parte 2: Questões de Pesquisa</h2>
            <div class="rq-box">
                <h3>RQ1</h3>
                <p>Qual a relação entre a popularidade (stars) de um repositório e seu nível de atividade?</p>
            </div>
            <div class="rq-box">
                <h3>RQ2</h3>
                <p>Existe diferença significativa na taxa de resolução de issues entre diferentes linguagens?</p>
            </div>
            <div class="rq-box">
                <h3>RQ3</h3>
                <p>Repositórios com documentação apresentam maior engajamento da comunidade?</p>
            </div>
            <div class="rq-box">
                <h3>RQ4</h3>
                <p>Como a escolha da licença impacta na popularidade e contribuição?</p>
            </div>
        </div>

        <div class="visualization"><h3>RQ1.1: Stars vs Commits</h3>{graficos['rq1']}</div>
        <div class="visualization"><h3>RQ1.2: Stars vs Contributors</h3>{graficos['rq2']}</div>
        <div class="visualization"><h3>RQ1.3: Matriz de Correlação</h3>{graficos['rq3']}</div>
        <div class="visualization"><h3>RQ2.1: Taxa de Resolução (Box Plot)</h3>{graficos['rq4']}</div>
        <div class="visualization"><h3>RQ2.2: Taxa de Resolução (Violin)</h3>{graficos['rq5']}</div>
        <div class="visualization"><h3>RQ2.3: Taxa Média de Resolução</h3>{graficos['rq6']}</div>
        <div class="visualization"><h3>RQ3.1: Documentação e Engajamento</h3>{graficos['rq7']}</div>
        <div class="visualization"><h3>RQ3.2: Documentação vs Stars</h3>{graficos['rq8']}</div>
        <div class="visualization"><h3>RQ4.1: Métricas por Licença</h3>{graficos['rq9']}</div>
        <div class="visualization"><h3>RQ4.2: Distribuição Stars por Licença</h3>{graficos['rq10']}</div>
        <div class="visualization"><h3>RQ4.3: Popularidade vs Contribuição</h3>{graficos['rq11']}</div>

        <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; text-align: center; margin-top: 30px; color: #666;">
            <p>Dashboard gerado em {datetime.now().strftime("%d/%m/%Y %H:%M")}</p>
            <p style="font-size: 0.9em;">Laboratório de Experimentação em Engenharia de Software - PUC</p>
        </div>
    </div>
</body>
</html>"""
    
    with open('dashboard_completo_sem_iframes.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("[OK] Dashboard sem iframes gerado: dashboard_completo_sem_iframes.html")
    print("\n[INFO] Este dashboard incorpora todos os graficos diretamente no HTML")
    print("[INFO] Nao ha problemas de CORS - funciona perfeitamente ao abrir localmente!")


def main():
    """Função principal"""
    df = pd.read_csv('dados_repositorios.csv')
    df['created_at'] = pd.to_datetime(df['created_at'])
    df['updated_at'] = pd.to_datetime(df['updated_at'])
    gerar_dashboard_sem_iframes(df)


if __name__ == "__main__":
    main()


