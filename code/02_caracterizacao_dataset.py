#!/usr/bin/env python3
"""
02_caracterizacao_dataset.py
- Verifica se existe 'data/repositorios.csv'. Se não existir, gera um dataset simulado e salva.
- Gera estatísticas descritivas e visualizações de caracterização exigidas pela Sprint 1:
    * quantidade de repositórios por linguagem (barra)
    * distribuição de stars (histograma)
    * boxplot de stars por linguagem
    * evolução temporal de criação (repositórios por mês)
- Salva estatísticas em JSON (outputs/estatisticas_gerais.json)
- Salva gráficos em outputs/
"""

import os
import json
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----- Configs de paths -----
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)
CSV_PATH = os.path.join(DATA_DIR, "repositorios.csv")

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----- Função de geração de dataset simulado (apenas fallback) -----
def gerar_dataset_simulado(n=500, seed=42):
    """
    Gera um DataFrame simulando métricas de repositórios GitHub.
    Colunas (úteis para análises posteriores): id, nome, linguagem, created_at,
    stars, forks, commits, contributors, issues_abertas, issues_fechadas, tem_docs (bool), licença
    """
    np.random.seed(seed)
    linguagens = ["Python", "JavaScript", "Java", "C++", "Go", "TypeScript", "Ruby", "C#"]
    nomes = [f"repo_{i}" for i in range(n)]
    linguagem = np.random.choice(linguagens, size=n, p=[0.25,0.2,0.15,0.1,0.08,0.08,0.07,0.07])
    # datas nos últimos 5 anos
    end = datetime.now()
    start = end - timedelta(days=5*365)
    created_at = [start + timedelta(days=int(x)) for x in np.random.uniform(0, (end-start).days, size=n)]
    # stars: mistura de lognormal para refletir skew
    stars = np.round(np.random.lognormal(mean=2.0, sigma=1.2, size=n)).astype(int)
    forks = np.round(stars * np.random.uniform(0.05, 0.5, size=n)).astype(int)
    commits = np.round(np.random.lognormal(mean=3.0, sigma=1.0, size=n)).astype(int)
    contributors = np.clip((np.random.poisson(2, size=n) + (stars//50)), 1, None)
    issues_abertas = np.random.poisson(5, size=n)
    issues_fechadas = np.minimum(issues_abertas + np.random.poisson(3, size=n), issues_abertas + 10)
    tem_docs = np.random.choice([True, False], size=n, p=[0.6, 0.4])
    licencas = np.random.choice(["MIT", "Apache-2.0", "GPL-3.0", "None", "BSD-3-Clause"], size=n, p=[0.35,0.2,0.15,0.2,0.1])
    df = pd.DataFrame({
        "id": range(1, n+1),
        "nome": nomes,
        "linguagem": linguagem,
        "created_at": pd.to_datetime(created_at),
        "stars": stars,
        "forks": forks,
        "commits": commits,
        "contributors": contributors,
        "issues_abertas": issues_abertas,
        "issues_fechadas": issues_fechadas,
        "tem_docs": tem_docs,
        "licenca": licencas
    })
    # taxa de resolução de issues
    df["taxa_resolucao_issues"] = df.apply(lambda r: (r.issues_fechadas / r.issues_abertas) if r.issues_abertas > 0 else np.nan, axis=1)
    return df

# ----- Ler CSV ou gerar -----
if os.path.exists(CSV_PATH):
    print(f"[INFO] Lendo dataset existente em: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH, parse_dates=["created_at"])
else:
    print(f"[WARN] Arquivo {CSV_PATH} não encontrado. Gerando dataset simulado e salvando.")
    df = gerar_dataset_simulado(n=600)
    df.to_csv(CSV_PATH, index=False)
    print(f"[INFO] Dataset simulado salvo em {CSV_PATH}")

# ----- Estatísticas gerais -----
estatisticas = {}
estatisticas["num_repositorios"] = int(len(df))
estatisticas["periodo"] = {
    "min_created_at": str(df["created_at"].min().date()),
    "max_created_at": str(df["created_at"].max().date())
}
estatisticas["linguagens_unicas"] = int(df["linguagem"].nunique())
estatisticas["top_5_linguagens"] = df["linguagem"].value_counts().head(5).to_dict()
estatisticas["stars_descritiva"] = df["stars"].describe().to_dict()
estatisticas["commits_descritiva"] = df["commits"].describe().to_dict()

with open(os.path.join(OUTPUT_DIR, "estatisticas_gerais.json"), "w", encoding="utf-8") as f:
    json.dump(estatisticas, f, indent=2)
print(f"[INFO] Estatísticas gerais salvas em outputs/estatisticas_gerais.json")

# ----- Visualizações (matplotlib) -----
# 1) Quantidade de repositórios por linguagem (barra)
vc = df["linguagem"].value_counts()
plt.figure(figsize=(8,5))
vc.plot(kind="bar")
plt.title("Quantidade de repositórios por linguagem")
plt.xlabel("Linguagem")
plt.ylabel("Número de repositórios")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "repos_por_linguagem_bar.png"))
plt.close()
print("[INFO] Gráfico 'repos_por_linguagem_bar.png' salvo.")

# 2) Distribuição de stars (histograma) - log scale nos eixos se necessário
plt.figure(figsize=(8,5))
plt.hist(df["stars"], bins=40)
plt.title("Distribuição de Stars")
plt.xlabel("Stars")
plt.ylabel("Frequência")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "distribuicao_stars_hist.png"))
plt.close()
print("[INFO] Gráfico 'distribuicao_stars_hist.png' salvo.")

# 3) Boxplot de stars por linguagem (mostra variação por linguagem)
plt.figure(figsize=(10,6))
# ordenar linguagens por mediana para melhor visualização
order = df.groupby("linguagem")["stars"].median().sort_values(ascending=False).index
df.boxplot(column="stars", by="linguagem", grid=False, rot=45, figsize=(10,6), order=list(order))
plt.suptitle("")  # remove título automático
plt.title("Boxplot de Stars por Linguagem")
plt.xlabel("Linguagem")
plt.ylabel("Stars")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "boxplot_stars_por_linguagem.png"))
plt.close()
print("[INFO] Gráfico 'boxplot_stars_por_linguagem.png' salvo.")

# 4) Evolução temporal: contagem de repositórios criados por mês
df["created_month"] = df["created_at"].dt.to_period("M").dt.to_timestamp()
monthly = df.groupby("created_month").size()
plt.figure(figsize=(10,4))
monthly.plot()
plt.title("Repositórios criados por mês")
plt.xlabel("Mês")
plt.ylabel("Número de repositórios")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "repos_por_mes_line.png"))
plt.close()
print("[INFO] Gráfico 'repos_por_mes_line.png' salvo.")

# 5) Tabela resumida por linguagem (média, mediana de stars, commits, contributors)
resumo_por_linguagem = df.groupby("linguagem").agg({
    "stars": ["count", "mean", "median", "std"],
    "commits": ["mean", "median"],
    "contributors": ["mean", "median"],
    "taxa_resolucao_issues": ["mean"]
})
resumo_por_linguagem.columns = ["_".join(c).strip() for c in resumo_por_linguagem.columns.values]
resumo_csv_path = os.path.join(OUTPUT_DIR, "resumo_por_linguagem.csv")
resumo_por_linguagem.to_csv(resumo_csv_path)
print(f"[INFO] Resumo por linguagem salvo em {resumo_csv_path}")

print("\n[CONCLUÍDO] Sprint 1 - caracterização gerada. Verifique a pasta outputs/ para os gráficos e arquivos.")
