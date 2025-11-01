"""
Script de coleta de dados de repositórios do GitHub
Laboratório 04 - Visualização de dados utilizando ferramenta de BI
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import json

# Configuração para reprodutibilidade
random.seed(42)
np.random.seed(42)

def gerar_dataset_repositorios(n_repos=500):
    """
    Gera um dataset simulado de repositórios do GitHub para análise.
    Em um cenário real, estes dados seriam coletados via GitHub API.
    """
    
    # Linguagens de programação mais populares
    linguagens = ['Python', 'JavaScript', 'Java', 'TypeScript', 'Go', 'Rust', 'C++', 'Ruby']
    linguagens_pesos = [0.25, 0.20, 0.15, 0.15, 0.10, 0.05, 0.05, 0.05]
    
    # Licenças comuns
    licencas = ['MIT', 'Apache-2.0', 'GPL-3.0', 'BSD-3-Clause', 'None']
    licencas_pesos = [0.45, 0.25, 0.15, 0.10, 0.05]
    
    # Categorias de projeto
    categorias = ['Web Development', 'Data Science', 'DevOps', 'Mobile', 'Machine Learning', 
                  'System Tools', 'Libraries', 'Games']
    
    dados = []
    
    for i in range(n_repos):
        # Seleciona linguagem
        linguagem = random.choices(linguagens, weights=linguagens_pesos)[0]
        
        # Define métricas baseadas na linguagem (algumas linguagens têm repos mais ativos)
        multiplicador_linguagem = {
            'Python': 1.5, 'JavaScript': 1.4, 'TypeScript': 1.3,
            'Java': 1.0, 'Go': 1.2, 'Rust': 1.1, 'C++': 0.9, 'Ruby': 0.8
        }
        mult = multiplicador_linguagem.get(linguagem, 1.0)
        
        # Gera métricas do repositório
        stars = int(np.random.lognormal(4, 2) * mult)
        forks = int(stars * np.random.uniform(0.05, 0.30))
        issues_abertas = int(np.random.poisson(max(10, stars * 0.02)))
        issues_fechadas = int(issues_abertas * np.random.uniform(2, 8))
        
        pull_requests = int(np.random.poisson(max(5, stars * 0.015)))
        contributors = int(np.random.lognormal(1.5, 1) * mult)
        commits = int(np.random.lognormal(5, 1.5) * mult)
        
        # Data de criação (últimos 5 anos)
        dias_atras = random.randint(30, 1825)  # 30 dias a 5 anos
        created_at = datetime.now() - timedelta(days=dias_atras)
        
        # Última atualização (entre criação e agora)
        dias_desde_update = random.randint(0, min(dias_atras, 365))
        updated_at = datetime.now() - timedelta(days=dias_desde_update)
        
        # Tamanho do repositório (KB)
        tamanho = int(np.random.lognormal(8, 2))
        
        # Tem documentação?
        tem_wiki = random.random() < 0.3
        tem_readme = random.random() < 0.9
        
        # Licença
        licenca = random.choices(licencas, weights=licencas_pesos)[0]
        
        # Categoria
        categoria = random.choice(categorias)
        
        # Nome do repositório
        nome = f"projeto-{linguagem.lower()}-{i+1:03d}"
        
        # Calcula idade em dias
        idade_dias = (datetime.now() - created_at).days
        
        # Calcula taxa de atividade (commits por mês)
        meses_existencia = max(idade_dias / 30, 1)
        commits_por_mes = commits / meses_existencia
        
        # Calcula taxa de resolução de issues
        total_issues = issues_abertas + issues_fechadas
        taxa_resolucao = (issues_fechadas / total_issues * 100) if total_issues > 0 else 0
        
        dados.append({
            'repositorio': nome,
            'linguagem': linguagem,
            'stars': stars,
            'forks': forks,
            'issues_abertas': issues_abertas,
            'issues_fechadas': issues_fechadas,
            'total_issues': total_issues,
            'taxa_resolucao_issues': round(taxa_resolucao, 2),
            'pull_requests': pull_requests,
            'contributors': contributors,
            'commits': commits,
            'commits_por_mes': round(commits_por_mes, 2),
            'tamanho_kb': tamanho,
            'created_at': created_at.strftime('%Y-%m-%d'),
            'updated_at': updated_at.strftime('%Y-%m-%d'),
            'idade_dias': idade_dias,
            'dias_desde_update': dias_desde_update,
            'tem_wiki': tem_wiki,
            'tem_readme': tem_readme,
            'licenca': licenca,
            'categoria': categoria
        })
    
    return pd.DataFrame(dados)


def main():
    """Função principal para coleta de dados"""
    
    print("=" * 70)
    print("LABORATÓRIO 04 - Coleta de Dados")
    print("=" * 70)
    print()
    
    # Gera o dataset
    print("Gerando dataset de repositórios do GitHub...")
    df = gerar_dataset_repositorios(n_repos=500)
    
    # Salva os dados
    df.to_csv('dados_repositorios.csv', index=False, encoding='utf-8')
    print(f"[OK] Dataset salvo: {len(df)} repositorios coletados")
    print(f"[OK] Arquivo: dados_repositorios.csv")
    print()
    
    # Exibe estatísticas básicas
    print("Resumo do Dataset:")
    print("-" * 70)
    print(f"Total de repositórios: {len(df)}")
    print(f"Linguagens: {df['linguagem'].nunique()}")
    print(f"Período: {df['created_at'].min()} a {df['created_at'].max()}")
    print()
    
    print("Distribuição por linguagem:")
    print(df['linguagem'].value_counts())
    print()
    
    print("Estatísticas de Stars:")
    print(df['stars'].describe())
    print()
    
    print("=" * 70)
    print("Coleta concluída com sucesso!")
    print("=" * 70)


if __name__ == "__main__":
    main()

