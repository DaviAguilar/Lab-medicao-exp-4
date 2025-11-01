"""
Script de análise das Questões de Pesquisa (RQs)
Laboratório 04 - Sprint 2: Visualizações para RQs
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import json


class AnaliseRQs:
    
    def __init__(self, arquivo_dados):
        """Inicializa com o arquivo de dados"""
        self.df = pd.read_csv(arquivo_dados)
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        self.df['updated_at'] = pd.to_datetime(self.df['updated_at'])
        
        # Define as RQs
        self.rqs = {
            'RQ1': 'Qual a relação entre a popularidade (stars) de um repositório e seu nível de atividade (commits e contributors)?',
            'RQ2': 'Existe diferença significativa na taxa de resolução de issues entre diferentes linguagens de programação?',
            'RQ3': 'Repositórios com documentação (wiki/readme) apresentam maior engajamento da comunidade?',
            'RQ4': 'Como a escolha da licença impacta na popularidade e contribuição dos repositórios?'
        }
    
    def exibir_rqs(self):
        """Exibe as questões de pesquisa"""
        print("\n" + "=" * 70)
        print("QUESTÕES DE PESQUISA (Research Questions)")
        print("=" * 70)
        
        for rq_id, rq_text in self.rqs.items():
            print(f"\n{rq_id}: {rq_text}")
        
        print("\n" + "=" * 70 + "\n")
    
    # ========== RQ1 ==========
    
    def analisar_rq1(self):
        """
        RQ1: Qual a relação entre a popularidade (stars) de um repositório 
        e seu nível de atividade (commits e contributors)?
        """
        
        print("\n" + "=" * 70)
        print("RQ1: RELAÇÃO ENTRE POPULARIDADE E ATIVIDADE")
        print("=" * 70 + "\n")
        
        # Calcula correlações
        corr_stars_commits = self.df['stars'].corr(self.df['commits'])
        corr_stars_contributors = self.df['stars'].corr(self.df['contributors'])
        
        print(f"Correlação Stars vs Commits: {corr_stars_commits:.3f}")
        print(f"Correlação Stars vs Contributors: {corr_stars_contributors:.3f}")
        
        # Visualização 1: Scatter plot Stars vs Commits
        fig1 = px.scatter(self.df, 
                         x='commits', 
                         y='stars',
                         color='linguagem',
                         size='contributors',
                         hover_data=['repositorio'],
                         title='RQ1.1: Relação entre Stars e Commits',
                         log_x=True,
                         log_y=True)
        
        fig1.update_layout(
            xaxis_title='Total de Commits (escala log)',
            yaxis_title='Stars (escala log)',
            height=600
        )
        
        fig1.write_html('rq01_stars_vs_commits.html')
        print("[OK] Visualizacao salva: rq01_stars_vs_commits.html")
        
        # Visualização 2: Scatter plot Stars vs Contributors
        fig2 = px.scatter(self.df, 
                         x='contributors', 
                         y='stars',
                         color='linguagem',
                         size='commits',
                         hover_data=['repositorio'],
                         title='RQ1.2: Relação entre Stars e Contributors',
                         log_x=True,
                         log_y=True)
        
        fig2.update_layout(
            xaxis_title='Número de Contributors (escala log)',
            yaxis_title='Stars (escala log)',
            height=600
        )
        
        fig2.write_html('rq02_stars_vs_contributors.html')
        print("[OK] Visualizacao salva: rq02_stars_vs_contributors.html")
        
        # Visualização 3: Heatmap de correlação
        metricas_correlacao = ['stars', 'forks', 'commits', 'contributors', 'pull_requests']
        corr_matrix = self.df[metricas_correlacao].corr()
        
        fig3 = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=metricas_correlacao,
            y=metricas_correlacao,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Correlação")
        ))
        
        fig3.update_layout(
            title='RQ1.3: Matriz de Correlação entre Métricas de Popularidade e Atividade',
            height=600,
            width=700
        )
        
        fig3.write_html('rq03_matriz_correlacao.html')
        print("[OK] Visualizacao salva: rq03_matriz_correlacao.html")
        
        # Salva resultados
        resultados_rq1 = {
            'correlacao_stars_commits': float(corr_stars_commits),
            'correlacao_stars_contributors': float(corr_stars_contributors),
            'interpretacao': 'Correlação positiva moderada a forte indica que repositórios mais populares tendem a ter mais atividade'
        }
        
        return resultados_rq1
    
    # ========== RQ2 ==========
    
    def analisar_rq2(self):
        """
        RQ2: Existe diferença significativa na taxa de resolução de issues 
        entre diferentes linguagens de programação?
        """
        
        print("\n" + "=" * 70)
        print("RQ2: TAXA DE RESOLUÇÃO DE ISSUES POR LINGUAGEM")
        print("=" * 70 + "\n")
        
        # Calcula estatísticas por linguagem
        stats_linguagem = self.df.groupby('linguagem').agg({
            'taxa_resolucao_issues': ['mean', 'median', 'std', 'count']
        }).round(2)
        
        print("Estatísticas de Taxa de Resolução por Linguagem:")
        print(stats_linguagem)
        print()
        
        # Teste estatístico (ANOVA)
        grupos = [group['taxa_resolucao_issues'].values for name, group in self.df.groupby('linguagem')]
        f_stat, p_value = stats.f_oneway(*grupos)
        
        print(f"Teste ANOVA:")
        print(f"  F-statistic: {f_stat:.4f}")
        print(f"  p-value: {p_value:.4f}")
        
        if p_value < 0.05:
            print("  [OK] Existe diferenca estatisticamente significativa (p < 0.05)")
        else:
            print("  [X] Nao existe diferenca estatisticamente significativa (p >= 0.05)")
        
        # Visualização 1: Box plot de taxa de resolução
        fig1 = px.box(self.df, 
                     x='linguagem', 
                     y='taxa_resolucao_issues',
                     color='linguagem',
                     title='RQ2.1: Taxa de Resolução de Issues por Linguagem',
                     points='outliers')
        
        fig1.update_layout(
            xaxis_title='Linguagem de Programação',
            yaxis_title='Taxa de Resolução de Issues (%)',
            showlegend=False,
            height=600
        )
        
        fig1.write_html('rq04_taxa_resolucao_boxplot.html')
        print("[OK] Visualizacao salva: rq04_taxa_resolucao_boxplot.html")
        
        # Visualização 2: Violin plot
        fig2 = px.violin(self.df, 
                        x='linguagem', 
                        y='taxa_resolucao_issues',
                        color='linguagem',
                        box=True,
                        title='RQ2.2: Distribuição da Taxa de Resolução de Issues',
                        points='all')
        
        fig2.update_layout(
            xaxis_title='Linguagem de Programação',
            yaxis_title='Taxa de Resolução de Issues (%)',
            showlegend=False,
            height=600
        )
        
        fig2.write_html('rq05_taxa_resolucao_violin.html')
        print("[OK] Visualizacao salva: rq05_taxa_resolucao_violin.html")
        
        # Visualização 3: Barras com média e desvio padrão
        media_por_linguagem = self.df.groupby('linguagem')['taxa_resolucao_issues'].agg(['mean', 'std']).reset_index()
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(
            x=media_por_linguagem['linguagem'],
            y=media_por_linguagem['mean'],
            error_y=dict(type='data', array=media_por_linguagem['std']),
            marker_color='steelblue',
            text=media_por_linguagem['mean'].round(1),
            texttemplate='%{text}%',
            textposition='outside'
        ))
        
        fig3.update_layout(
            title='RQ2.3: Taxa Média de Resolução de Issues por Linguagem (com desvio padrão)',
            xaxis_title='Linguagem de Programação',
            yaxis_title='Taxa Média de Resolução (%)',
            height=600
        )
        
        fig3.write_html('rq06_taxa_resolucao_media.html')
        print("[OK] Visualizacao salva: rq06_taxa_resolucao_media.html")
        
        resultados_rq2 = {
            'anova_f_statistic': float(f_stat),
            'anova_p_value': float(p_value),
            'significativo': bool(p_value < 0.05),
            'media_por_linguagem': media_por_linguagem.set_index('linguagem')['mean'].to_dict()
        }
        
        return resultados_rq2
    
    # ========== RQ3 ==========
    
    def analisar_rq3(self):
        """
        RQ3: Repositórios com documentação (wiki/readme) apresentam 
        maior engajamento da comunidade?
        """
        
        print("\n" + "=" * 70)
        print("RQ3: IMPACTO DA DOCUMENTAÇÃO NO ENGAJAMENTO")
        print("=" * 70 + "\n")
        
        # Cria grupos baseado em documentação
        self.df['nivel_documentacao'] = 'Nenhuma'
        self.df.loc[self.df['tem_readme'] == True, 'nivel_documentacao'] = 'README'
        self.df.loc[(self.df['tem_readme'] == True) & (self.df['tem_wiki'] == True), 'nivel_documentacao'] = 'README + Wiki'
        
        # Compara métricas de engajamento
        metricas_engajamento = ['stars', 'forks', 'contributors', 'pull_requests']
        
        comparacao = self.df.groupby('nivel_documentacao')[metricas_engajamento].median().reset_index()
        
        print("Mediana de Engajamento por Nível de Documentação:")
        print(comparacao)
        print()
        
        # Testes estatísticos
        grupos_readme = self.df[self.df['tem_readme'] == True]['stars'].values
        grupos_sem_readme = self.df[self.df['tem_readme'] == False]['stars'].values
        
        u_stat, p_value = stats.mannwhitneyu(grupos_readme, grupos_sem_readme, alternative='greater')
        
        print(f"Teste Mann-Whitney U (README vs Sem README):")
        print(f"  U-statistic: {u_stat:.4f}")
        print(f"  p-value: {p_value:.4f}")
        
        if p_value < 0.05:
            print("  [OK] Repositorios com README tem significativamente mais stars (p < 0.05)")
        else:
            print("  [X] Diferenca nao significativa (p >= 0.05)")
        
        # Visualização 1: Comparação de métricas
        fig1 = make_subplots(rows=2, cols=2,
                            subplot_titles=('Stars', 'Forks', 'Contributors', 'Pull Requests'))
        
        colors = {'Nenhuma': 'red', 'README': 'orange', 'README + Wiki': 'green'}
        
        for idx, metrica in enumerate(metricas_engajamento):
            row = idx // 2 + 1
            col = idx % 2 + 1
            
            dados = self.df.groupby('nivel_documentacao')[metrica].median().reset_index()
            
            fig1.add_trace(
                go.Bar(x=dados['nivel_documentacao'], 
                       y=dados[metrica],
                       name=metrica,
                       marker_color=[colors[x] for x in dados['nivel_documentacao']],
                       showlegend=False),
                row=row, col=col
            )
        
        fig1.update_layout(
            title_text='RQ3.1: Métricas de Engajamento por Nível de Documentação (Mediana)',
            height=800
        )
        
        fig1.write_html('rq07_documentacao_engajamento.html')
        print("[OK] Visualizacao salva: rq07_documentacao_engajamento.html")
        
        # Visualização 2: Box plot comparativo
        fig2 = px.box(self.df, 
                     x='nivel_documentacao', 
                     y='stars',
                     color='nivel_documentacao',
                     title='RQ3.2: Distribuição de Stars por Nível de Documentação',
                     log_y=True,
                     color_discrete_map=colors)
        
        fig2.update_layout(
            xaxis_title='Nível de Documentação',
            yaxis_title='Stars (escala log)',
            showlegend=False,
            height=600
        )
        
        fig2.write_html('rq08_documentacao_stars.html')
        print("[OK] Visualizacao salva: rq08_documentacao_stars.html")
        
        resultados_rq3 = {
            'mann_whitney_u': float(u_stat),
            'p_value': float(p_value),
            'significativo': bool(p_value < 0.05),
            'mediana_por_nivel': comparacao.set_index('nivel_documentacao')['stars'].to_dict()
        }
        
        return resultados_rq3
    
    # ========== RQ4 ==========
    
    def analisar_rq4(self):
        """
        RQ4: Como a escolha da licença impacta na popularidade 
        e contribuição dos repositórios?
        """
        
        print("\n" + "=" * 70)
        print("RQ4: IMPACTO DA LICENÇA NA POPULARIDADE E CONTRIBUIÇÃO")
        print("=" * 70 + "\n")
        
        # Estatísticas por licença
        stats_licenca = self.df.groupby('licenca').agg({
            'stars': 'median',
            'forks': 'median',
            'contributors': 'median',
            'repositorio': 'count'
        }).round(2)
        stats_licenca.columns = ['Stars (mediana)', 'Forks (mediana)', 'Contributors (mediana)', 'Quantidade']
        
        print("Estatísticas por Licença:")
        print(stats_licenca)
        print()
        
        # Visualização 1: Comparação de popularidade por licença
        fig1 = go.Figure()
        
        medianas = self.df.groupby('licenca').agg({
            'stars': 'median',
            'forks': 'median',
            'contributors': 'median'
        }).reset_index()
        
        fig1.add_trace(go.Bar(
            name='Stars',
            x=medianas['licenca'],
            y=medianas['stars'],
            marker_color='gold'
        ))
        
        fig1.add_trace(go.Bar(
            name='Forks',
            x=medianas['licenca'],
            y=medianas['forks'],
            marker_color='lightblue'
        ))
        
        fig1.add_trace(go.Bar(
            name='Contributors',
            x=medianas['licenca'],
            y=medianas['contributors'],
            marker_color='lightgreen'
        ))
        
        fig1.update_layout(
            title='RQ4.1: Métricas por Tipo de Licença (Mediana)',
            xaxis_title='Tipo de Licença',
            yaxis_title='Valor (mediana)',
            barmode='group',
            height=600
        )
        
        fig1.write_html('rq09_licenca_metricas.html')
        print("[OK] Visualizacao salva: rq09_licenca_metricas.html")
        
        # Visualização 2: Distribuição de stars por licença
        fig2 = px.violin(self.df, 
                        x='licenca', 
                        y='stars',
                        color='licenca',
                        box=True,
                        title='RQ4.2: Distribuição de Stars por Tipo de Licença',
                        log_y=True,
                        points='outliers')
        
        fig2.update_layout(
            xaxis_title='Tipo de Licença',
            yaxis_title='Stars (escala log)',
            showlegend=False,
            height=600
        )
        
        fig2.write_html('rq10_licenca_stars_distribuicao.html')
        print("[OK] Visualizacao salva: rq10_licenca_stars_distribuicao.html")
        
        # Visualização 3: Scatter plot - Popularidade vs Contribuição por Licença
        fig3 = px.scatter(self.df, 
                         x='stars', 
                         y='contributors',
                         color='licenca',
                         size='forks',
                         hover_data=['repositorio'],
                         title='RQ4.3: Popularidade vs Contribuição por Tipo de Licença',
                         log_x=True,
                         log_y=True)
        
        fig3.update_layout(
            xaxis_title='Stars (escala log)',
            yaxis_title='Contributors (escala log)',
            height=600
        )
        
        fig3.write_html('rq11_licenca_popularidade_contribuicao.html')
        print("[OK] Visualizacao salva: rq11_licenca_popularidade_contribuicao.html")
        
        resultados_rq4 = {
            'medianas_por_licenca': medianas.set_index('licenca').to_dict()
        }
        
        return resultados_rq4
    
    def executar_analise_completa(self):
        """Executa análise completa de todas as RQs"""
        
        self.exibir_rqs()
        
        print("\n" + "=" * 70)
        print("INICIANDO ANÁLISE DAS QUESTÕES DE PESQUISA")
        print("=" * 70)
        
        resultados = {}
        
        # Analisa cada RQ
        resultados['RQ1'] = self.analisar_rq1()
        resultados['RQ2'] = self.analisar_rq2()
        resultados['RQ3'] = self.analisar_rq3()
        resultados['RQ4'] = self.analisar_rq4()
        
        # Salva todos os resultados
        with open('resultados_rqs.json', 'w') as f:
            json.dump(resultados, f, indent=2, default=str)
        
        print("\n" + "=" * 70)
        print("ANÁLISE COMPLETA CONCLUÍDA!")
        print("Resultados salvos em: resultados_rqs.json")
        print("=" * 70)
        
        return resultados


def main():
    """Função principal"""
    
    analise = AnaliseRQs('dados_repositorios.csv')
    analise.executar_analise_completa()


if __name__ == "__main__":
    main()

