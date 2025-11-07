#!/usr/bin/env python3
import os
import json
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.io as pio

# ===== Paths =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "..", "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

csv_path = os.path.join(DATA_DIR, "metricas_engajamento.csv")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Arquivo {csv_path} não encontrado! Verifique se o CSV foi gerado corretamente.")

# ===== Carregar dataset =====
df = pd.read_csv(csv_path)

# renomear colunas relevantes
df = df.rename(columns={
    "language": "linguagem",
    "issue_resolution_rate": "taxa_resolucao_issues"
})

# descartar repositórios sem linguagem definida
df = df.dropna(subset=["linguagem"])

print(f"[INFO] Dataset carregado com {len(df)} repositórios e {len(df.columns)} colunas.")
print("Colunas principais:", ", ".join(df.columns[:10]), "...")

# ===========================================================
# RQ1: Popularidade (stars) x Atividade (commits, contributors)
# ===========================================================

def analisar_rq1(df):
    print("\n[RQ1] Iniciando análise: Popularidade (stars) x Atividade (commits, contributors)")
    sub = df.dropna(subset=["stars", "commits", "contributors"])

    # correlações
    pearson_commits = stats.pearsonr(sub["stars"], sub["commits"])
    spearman_commits = stats.spearmanr(sub["stars"], sub["commits"])
    pearson_contrib = stats.pearsonr(sub["stars"], sub["contributors"])
    spearman_contrib = stats.spearmanr(sub["stars"], sub["contributors"])

    print(f"Pearson (stars x commits): r={pearson_commits[0]:.3f}, p={pearson_commits[1]:.3e}")
    print(f"Spearman (stars x commits): rho={spearman_commits.correlation:.3f}, p={spearman_commits.pvalue:.3e}")
    print(f"Pearson (stars x contributors): r={pearson_contrib[0]:.3f}, p={pearson_contrib[1]:.3e}")
    print(f"Spearman (stars x contributors): rho={spearman_contrib.correlation:.3f}, p={spearman_contrib.pvalue:.3e}")

    # Scatter: stars x commits
    plt.figure(figsize=(7,5))
    plt.scatter(sub["commits"], sub["stars"], alpha=0.6)
    m, b = np.polyfit(sub["commits"], sub["stars"], 1)
    xs = np.linspace(sub["commits"].min(), sub["commits"].max(), 100)
    plt.plot(xs, m*xs + b, linestyle="--", color="red")
    plt.xlabel("Commits")
    plt.ylabel("Stars")
    plt.title("Stars x Commits (com tendência linear)")
    plt.tight_layout()
    path1 = os.path.join(OUTPUT_DIR, "rq1_stars_x_commits_scatter.png")
    plt.savefig(path1)
    plt.close()

    # Scatter: stars x contributors
    plt.figure(figsize=(7,5))
    plt.scatter(sub["contributors"], sub["stars"], alpha=0.6)
    m2, b2 = np.polyfit(sub["contributors"], sub["stars"], 1)
    xs2 = np.linspace(sub["contributors"].min(), sub["contributors"].max(), 100)
    plt.plot(xs2, m2*xs2 + b2, linestyle="--", color="red")
    plt.xlabel("Contributors")
    plt.ylabel("Stars")
    plt.title("Stars x Contributors (com tendência linear)")
    plt.tight_layout()
    path2 = os.path.join(OUTPUT_DIR, "rq1_stars_x_contributors_scatter.png")
    plt.savefig(path2)
    plt.close()

    print(f"[RQ1] Gráficos salvos: {path1}, {path2}")

    # Plotly interativo (stars x commits colorizado por linguagem)
    try:
        fig = px.scatter(
            sub,
            x="commits",
            y="stars",
            color="linguagem",
            hover_data=["full_name", "forks", "contributors"],
            title="RQ1: Stars x Commits (interativo) — colorido por linguagem"
        )
        html_path = os.path.join(OUTPUT_DIR, "rq1_stars_x_commits_interactive.html")
        pio.write_html(fig, file=html_path, auto_open=False)
        print(f"[RQ1] HTML interativo salvo em {html_path}")
    except Exception as e:
        print(f"[RQ1] Falha ao gerar gráfico interativo: {e}")

    return {
        "pearson_stars_commits": pearson_commits[0],
        "spearman_stars_commits": spearman_commits.correlation,
        "pearson_stars_contributors": pearson_contrib[0],
        "spearman_stars_contributors": spearman_contrib.correlation,
        "regression_commits": {"slope": float(m), "intercept": float(b)},
        "regression_contributors": {"slope": float(m2), "intercept": float(b2)},
    }

# ===========================================================
# RQ2: Taxa de resolução de issues por linguagem
# ===========================================================

def analisar_rq2(df):
    print("\n[RQ2] Iniciando análise: Taxa de resolução de issues por linguagem")

    # Filtrar linguagens com número mínimo de repositórios para estabilidade (ex.: >= 10)
    contagem = df["linguagem"].value_counts()
    linguagens_validas = contagem[contagem >= 10].index.tolist()
    sub = df[df["linguagem"].isin(linguagens_validas)].dropna(subset=["taxa_resolucao_issues"])

    # Ordenar linguagens pela mediana da taxa de resolução
    order = sub.groupby("linguagem")["taxa_resolucao_issues"].median().sort_values(ascending=False).index

    plt.figure(figsize=(10, 6))
    sub_sorted = sub.copy()
    sub_sorted["linguagem"] = pd.Categorical(sub_sorted["linguagem"], categories=order, ordered=True)
    sub_sorted = sub_sorted.sort_values("linguagem")

    # Gerar o boxplot (sem o argumento 'order', que causava erro)
    sub_sorted.boxplot(column="taxa_resolucao_issues", by="linguagem", grid=False, rot=45)

    plt.suptitle("")
    plt.title("Taxa de resolução de issues por linguagem")
    plt.xlabel("Linguagem")
    plt.ylabel("Taxa de resolução (issues fechadas / abertas)")
    plt.tight_layout()

    # Salvar gráfico
    path_box = os.path.join(OUTPUT_DIR, "rq2_taxa_resolucao_boxplot.png")
    plt.savefig(path_box)
    plt.close()
    print(f"[RQ2] Boxplot salvo em {path_box}")

    # Teste estatístico: Kruskal-Wallis (não-paramétrico) entre os grupos
    grupos = [g["taxa_resolucao_issues"].dropna().values for _, g in sub.groupby("linguagem")]
    kw_stat, kw_p = None, None
    if len(grupos) >= 2:
        kw_stat, kw_p = stats.kruskal(*grupos)
        print(f"[RQ2] Kruskal-Wallis: stat={kw_stat:.3f}, p={kw_p:.3e}")
    else:
        print("[RQ2] Poucos grupos válidos para teste estatístico (menos de 2 linguagens).")

    # Resumo por linguagem (média, mediana, etc.)
    resumo = sub.groupby("linguagem")["taxa_resolucao_issues"].agg(["count", "mean", "median", "std"]).sort_values("median", ascending=False)
    resumo_path = os.path.join(OUTPUT_DIR, "rq2_resumo_taxa_resolucao_por_linguagem.csv")
    resumo.to_csv(resumo_path)
    print(f"[RQ2] Resumo salvo em {resumo_path}")

    return {"kruskal_stat": kw_stat, "kruskal_p": kw_p, "resumo_csv": resumo_path}

# ===========================================================
# Execução principal
# ===========================================================

if __name__ == "__main__":
    resultados = {}
    resultados["rq1"] = analisar_rq1(df)
    resultados["rq2"] = analisar_rq2(df)

    resumo_json_path = os.path.join(OUTPUT_DIR, "resumo_rqs.json")
    with open(resumo_json_path, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2)
    print(f"\n[CONCLUÍDO] RQ1 e RQ2 processadas. Resumo salvo em {resumo_json_path}")
    print("Arquivos gerados estão em 'outputs/'. Use-os no dashboard e no artigo (Seção 4: Resultados).")
