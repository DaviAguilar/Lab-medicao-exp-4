"""
Script de caracterização do dataset
Laboratório 04 - Sprint 1: Caracterização do Dataset
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

# Configurações de estilo
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

class CaracterizacaoDataset:
    
    def __init__(self, arquivo_dados):
        """Inicializa com o arquivo de dados"""
        self.df = pd.read_csv(arquivo_dados)
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        self.df['updated_at'] = pd.to_datetime(self.df['updated_at'])
        
    def gerar_estatisticas_gerais(self):
        """Gera estatísticas gerais do dataset"""
        
        print("=" * 70)
        print("CARACTERIZAÇÃO DO DATASET - ESTATÍSTICAS GERAIS")
        print("=" * 70)
        print()
        
        print(f"Total de repositorios: {len(self.df)}")
        print(f"Periodo de criacao: {self.df['created_at'].min().date()} a {self.df['created_at'].max().date()}")
        print(f"Linguagens de programacao: {self.df['linguagem'].nunique()}")
        print(f"Categorias: {self.df['categoria'].nunique()}")
        print()
        
        print("Distribuição por Linguagem:")
        print(self.df['linguagem'].value_counts())
        print()
        
        # Salva estatísticas em JSON
        stats = {
            'total_repositorios': int(len(self.df)),
            'linguagens': int(self.df['linguagem'].nunique()),
            'categorias': int(self.df['categoria'].nunique()),
            'periodo_inicio': str(self.df['created_at'].min().date()),
            'periodo_fim': str(self.df['created_at'].max().date()),
            'distribuicao_linguagens': self.df['linguagem'].value_counts().to_dict()
        }
        
        with open('estatisticas_gerais.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        return stats
    
    def visualizar_distribuicao_linguagens(self):
        """Visualização 1: Distribuição de repositórios por linguagem"""
        
        # Conta repositórios por linguagem
        lang_counts = self.df['linguagem'].value_counts().reset_index()
        lang_counts.columns = ['Linguagem', 'Quantidade']
        
        # Gráfico de barras interativo
        fig = px.bar(lang_counts, 
                     x='Linguagem', 
                     y='Quantidade',
                     title='Distribuição de Repositórios por Linguagem de Programação',
                     color='Quantidade',
                     color_continuous_scale='Viridis',
                     text='Quantidade')
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title='Linguagem de Programação',
            yaxis_title='Número de Repositórios',
            showlegend=False,
            height=500
        )
        
        fig.write_html('viz01_distribuicao_linguagens.html')
        print("[OK] Visualizacao salva: viz01_distribuicao_linguagens.html")
        
        return fig
    
    def visualizar_metricas_popularidade(self):
        """Visualização 2: Métricas de popularidade por linguagem"""
        
        # Calcula médias por linguagem
        metricas = self.df.groupby('linguagem').agg({
            'stars': 'median',
            'forks': 'median',
            'contributors': 'median'
        }).reset_index()
        
        # Gráfico de barras agrupadas
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Stars (mediana)',
            x=metricas['linguagem'],
            y=metricas['stars'],
            marker_color='gold'
        ))
        
        fig.add_trace(go.Bar(
            name='Forks (mediana)',
            x=metricas['linguagem'],
            y=metricas['forks'],
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Bar(
            name='Contributors (mediana)',
            x=metricas['linguagem'],
            y=metricas['contributors'],
            marker_color='lightgreen'
        ))
        
        fig.update_layout(
            title='Métricas de Popularidade por Linguagem (Mediana)',
            xaxis_title='Linguagem de Programação',
            yaxis_title='Valor (mediana)',
            barmode='group',
            height=500
        )
        
        fig.write_html('viz02_metricas_popularidade.html')
        print("[OK] Visualizacao salva: viz02_metricas_popularidade.html")
        
        return fig
    
    def visualizar_distribuicao_stars(self):
        """Visualização 3: Distribuição de stars (Box Plot)"""
        
        fig = px.box(self.df, 
                     x='linguagem', 
                     y='stars',
                     title='Distribuição de Stars por Linguagem',
                     color='linguagem',
                     log_y=True)
        
        fig.update_layout(
            xaxis_title='Linguagem de Programação',
            yaxis_title='Stars (escala logarítmica)',
            showlegend=False,
            height=500
        )
        
        fig.write_html('viz03_distribuicao_stars.html')
        print("[OK] Visualizacao salva: viz03_distribuicao_stars.html")
        
        return fig
    
    def visualizar_timeline_criacao(self):
        """Visualização 4: Timeline de criação de repositórios"""
        
        # Agrupa por mês e linguagem
        self.df['ano_mes'] = self.df['created_at'].dt.to_period('M')
        timeline = self.df.groupby(['ano_mes', 'linguagem']).size().reset_index(name='quantidade')
        timeline['ano_mes'] = timeline['ano_mes'].astype(str)
        
        fig = px.line(timeline, 
                      x='ano_mes', 
                      y='quantidade',
                      color='linguagem',
                      title='Timeline de Criação de Repositórios por Linguagem',
                      markers=True)
        
        fig.update_layout(
            xaxis_title='Período (Ano-Mês)',
            yaxis_title='Número de Repositórios Criados',
            height=500,
            xaxis={'tickangle': -45}
        )
        
        fig.write_html('viz04_timeline_criacao.html')
        print("[OK] Visualizacao salva: viz04_timeline_criacao.html")
        
        return fig
    
    def visualizar_atividade_repositorios(self):
        """Visualização 5: Atividade dos repositórios"""
        
        fig = px.scatter(self.df, 
                        x='idade_dias', 
                        y='commits',
                        color='linguagem',
                        size='contributors',
                        hover_data=['repositorio', 'stars'],
                        title='Atividade dos Repositórios: Commits vs Idade',
                        log_y=True)
        
        fig.update_layout(
            xaxis_title='Idade do Repositório (dias)',
            yaxis_title='Total de Commits (escala logarítmica)',
            height=600
        )
        
        fig.write_html('viz05_atividade_repositorios.html')
        print("[OK] Visualizacao salva: viz05_atividade_repositorios.html")
        
        return fig
    
    def visualizar_distribuicao_licencas(self):
        """Visualização 6: Distribuição de licenças"""
        
        licencas = self.df['licenca'].value_counts().reset_index()
        licencas.columns = ['Licença', 'Quantidade']
        
        fig = px.pie(licencas, 
                     values='Quantidade', 
                     names='Licença',
                     title='Distribuição de Licenças nos Repositórios',
                     hole=0.3)
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=500)
        
        fig.write_html('viz06_distribuicao_licencas.html')
        print("[OK] Visualizacao salva: viz06_distribuicao_licencas.html")
        
        return fig
    
    def visualizar_categorias(self):
        """Visualização 7: Distribuição por categoria"""
        
        categorias = self.df['categoria'].value_counts().reset_index()
        categorias.columns = ['Categoria', 'Quantidade']
        
        fig = px.bar(categorias, 
                     x='Quantidade', 
                     y='Categoria',
                     orientation='h',
                     title='Distribuição de Repositórios por Categoria',
                     color='Quantidade',
                     color_continuous_scale='Blues',
                     text='Quantidade')
        
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        fig.update_layout(
            xaxis_title='Número de Repositórios',
            yaxis_title='Categoria',
            showlegend=False,
            height=500
        )
        
        fig.write_html('viz07_distribuicao_categorias.html')
        print("[OK] Visualizacao salva: viz07_distribuicao_categorias.html")
        
        return fig
    
    def gerar_caracterizacao_completa(self):
        """Gera todas as visualizações de caracterização"""
        
        print("\n" + "=" * 70)
        print("GERANDO CARACTERIZAÇÃO COMPLETA DO DATASET")
        print("=" * 70 + "\n")
        
        self.gerar_estatisticas_gerais()
        
        print("\nGerando visualizações...")
        print("-" * 70)
        
        self.visualizar_distribuicao_linguagens()
        self.visualizar_metricas_popularidade()
        self.visualizar_distribuicao_stars()
        self.visualizar_timeline_criacao()
        self.visualizar_atividade_repositorios()
        self.visualizar_distribuicao_licencas()
        self.visualizar_categorias()
        
        print("\n" + "=" * 70)
        print("CARACTERIZAÇÃO CONCLUÍDA!")
        print("=" * 70)


def main():
    """Função principal"""
    
    caracterizacao = CaracterizacaoDataset('dados_repositorios.csv')
    caracterizacao.gerar_caracterizacao_completa()


if __name__ == "__main__":
    main()

