# Engajamento e Colaboração em Repositórios Open Source no GitHub

### Alunos:
- André Almeida Silva  
- Davi Aguilar Nunes Oliveira  

---

## 1. Introdução

O GitHub tornou-se o principal ambiente para desenvolvimento colaborativo de software. Seus repositórios não representam apenas armazenamento de código, mas **comunidades ativas**, onde desenvolvedores interagem, reportam problemas, revisam código e contribuem para a evolução do projeto.

No entanto, **não está claro quais fatores realmente indicam engajamento comunitário**. Estrelas (stars) refletem visibilidade, mas **representam colaboração real?**

Este estudo tem como objetivo **investigar padrões de engajamento e colaboração em repositórios open source**, utilizando dados de **1.000 repositórios ativos do GitHub**. O estudo é guiado pelo modelo **GQM (Goal–Question–Metrics)**:

| ID | Questão de Pesquisa |
|----|---------------------|
| **Q1** | Popularidade (estrelas) está relacionada ao número de contribuidores? |
| **Q2** | Há contribuição ativa da comunidade por meio de pull requests? |
| **Q3** | Os mantenedores respondem rapidamente às issues? |

---

## 2. Trabalhos Relacionados

Diversos estudos foram considerados como base teórica:

- **Popularidade ≠ engajamento real** — Tov et al. (2018) indicam que muitos usuários dão estrela, mas nunca interagem com o projeto.
- **Critérios para identificar repositórios realmente ativos** — Arachchi & Perera (2018) definem métricas mínimas de atividade, usadas também neste estudo.
- **Contribuição externa é relevante**, mas muitas vezes subestimada — Padhye et al. (2014).
- **Tempo de resposta influencia retenção de contribuidores** — Yu et al. (2024).

Esses trabalhos sustentam a hipótese de que **popularidade isolada é insuficiente para medir engajamento**.

---

## 3. Metodologia

### 3.1 Coleta e Ferramentas
A coleta dos dados foi feita via **GitHub REST API v3** e parcialmente via **GraphQL**, usando scripts Python desenvolvidos especificamente para este estudo.

### 3.2 Critérios de Inclusão — Repositórios Ativos
Com base em Arachchi & Perera (2018), um repositório só foi incluído se atendesse **todos** os critérios abaixo:

| Critério | Condição |
|----------|----------|
| Idade | ≥ 1 ano |
| Contribuidores | ≥ 5 |
| Stars | > 100 |
| Commits | > 50 |
| Forks | > 10 |
| Issues fechadas | > 50 |
| Último commit | ≤ 180 dias |
| Issues abertas | > 1 |

### 3.3 Métricas Coletadas
- Estrelas (stars)  
- Número de contribuidores  
- Pull requests (abertos, aceitos, rejeitados)  
- Tempo de resposta às issues  
- Issues abertas e fechadas  
- Linguagem principal  
- Dias desde o último commit  

### 3.4 Estrutura da Análise (GQM)

| RQ | Métrica(s) analisadas |
|----|------------------------|
| **Q1** | Stars × Número de contribuidores |
| **Q2** | PRs aceitos/rejeitados/abertos no último ano |
| **Q3** | Tempo de resposta + razão issues abertas/fechadas |

Todas as visualizações foram construídas em um **dashboard separado** (entregue conforme solicitado pela atividade).

---

## 4. Resultados

### **RQ1 — Popularidade implica maior número de contribuidores?**

Observou-se uma **correlação positiva, porém fraca e inconsistente**.  
Projetos com muitas estrelas nem sempre possuem uma comunidade proporcionalmente grande.

**Conclusão**: estrelas indicam visibilidade, mas **não garantem engajamento real**.

---

### **RQ2 — Há contribuição externa significativa?**

A análise de pull requests mostrou que a maioria dos projetos possui participação ativa da comunidade, com **mediana de 357 PRs aceitos** no último ano.  
Entretanto, houve **alta variação** entre os repositórios — poucos concentram a maioria das contribuições.

**Conclusão**: existe contribuição ativa, mas ela depende fortemente da governança e organização do projeto.

---

### **RQ3 — Mantenedores respondem rapidamente às issues?**

A maioria das issues recebeu uma resposta em **até 3 dias**, indicando responsividade e processos de comunicação eficazes.  
Além disso, observou-se uma **razão mediana de 11:1 entre issues fechadas e abertas**, indicando boa manutenção e histórico de resolução de problemas.

**Conclusão**: tempo de resposta é um dos melhores indicadores de engajamento saudável.

---

## 5. Conclusões

Os resultados mostram que:

| Questão | Resposta |
|--------|-----------|
| **RQ1** | Popularidade não indica engajamento comunitário. |
| **RQ2** | Contribuição externa ocorre, mas de forma desigual. |
| **RQ3** | Tempo de resposta é o melhor indicador de engajamento. |

Portanto, **comunidades engajadas não dependem apenas de visibilidade**, mas sim de:
- Boas práticas de governança;
- Processos claros para contribuição externa;
- Respostas rápidas às interações da comunidade.

Esse estudo pode servir como base para **estratégias de fortalecimento de repositórios open source** e para **novas investigações em Engenharia de Software Social**.

---

## Referências

- Borges, H., Hora, A., Valente, M.T. (2016). *Understanding the factors that impact the popularity of GitHub repositories.*
- Tov, M.T. et al. (2018). *What’s in a GitHub star?*
- Arachchi, S., Perera, I. (2018). *Uncovering the hidden patterns of contributor engagements.*
- Padhye, R. et al. (2014). *A study of external community contribution to open-source projects on GitHub.*
- Yu, Y. et al. (2024). *Predicting the first response latency of maintainers.*
- Rahman, M.M., Roy, C.K. (2014). *Issue template usage in large-scale GitHub projects.*

---
