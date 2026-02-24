# Cubo Mágico 2x2 — Grupo 3

Este projeto apresenta um agente inteligente capaz de resolver o Cubo Mágico 2x2 através de algoritmos de busca informada. A solução foi desenvolvida utilizando a biblioteca [aima-python](https://github.com/aimacode/aima-python).

O diferencial da implementação reside na integração de uma função heurística admissível com a técnica de canonicalização por rotação. Esta abordagem permite que o agente trate estados simétricos (equivalentes por rotação no espaço) como um único nó no grafo de busca, reduzindo drasticamente a explosão combinatória e otimizando o desempenho do algoritmo A*.

---

## Integrantes:

* Augusto Henrique da Silva Santana
* Cézar Augusto Nascimento Dias
* Gabriela Safira Neves de Oliveira
* Thiago Menezes Vasconcelos

---

* **Vídeo da Apresentação:** [Clique aqui para assistir](https://youtu.be/95ApSHbQmUA)

---

## Estrutura do Projeto

```
.
├── aima-python/          ← dependência (clonar conforme instruções)
├── env/
│   ├── __init__.py
│   ├── cube_env.py       ← estado, movimentos, permutações
|   ├── canonicalize.py   ← canonicalização por rotação do cubo
│   └── display.py        ← criar uma representação visual bidimensional das seis faces do cubo
├── solver/
│   ├── __init__.py
│   └── cubo_agent.py     ← NodeCubo, heurística h, A*, BFS
├── problems/
│   ├── __init__.py
│   └── cubo_problem.py   ← subclasse de Problem (aima)
├── tests/
│   ├── __init__.py
│   └── test_cubo.py      ← testes com pytest
├── main.py               ← ponto de entrada
└── README.md
```

---

##  Especificação Formal do Problema

A modelagem do problema segue o modelo clássico de busca da biblioteca AIMA:

### ● Representação dos Estados

* **Definição:** O estado é representado por uma **tupla de 24 stickers** (strings), onde cada posição do vetor corresponde a uma face e posição específica do cubo.
* **Mapeamento no Código:** Definido no arquivo `env/cube_env.py`. O dicionário `INDICES` mapeia as faces (DOWN, LEFT, BACK, UP, RIGHT, FRONT) para os índices de 0 a 23.

### ● Estado Inicial

* **Definição:** Um cubo em qualquer configuração configurada, podendo ser o estado resolvido ou um estado gerado por uma sequência de movimentos aleatórios.
* **Mapeamento no Código:** Implementado em `main.py` através da função `shuffle(ESTADO_INICIAL, n=30)`, que aplica 30 movimentos aleatórios para garantir complexidade de busca.

### ● Conjunto de Ações

* **Definição:** O conjunto de 12 rotações possíveis (6 faces × 2 direções: Horário e Anti-Horário).
* **Mapeamento no Código:** Definido em `problems/cubo_problem.py` dentro do método `actions(self, state)`, que retorna a lista de movimentos `TURNS`.

### ● Modelo de Transição (`result(s, a)`)

* **Definição:** Uma função que recebe um estado e uma ação e retorna o novo estado resultante da aplicação física da rotação.
* **Mapeamento no Código:** Implementado no método `result(self, state, action)` em `problems/cubo_problem.py`, que por sua vez utiliza a função `apply_move(state, face, direction)` de `env/cube_env.py` para permutar os stickers.

### ● Teste de Objetivo (`goal_test`)

* **Definição:** Verifica se o estado atual é o estado resolvido (todas as 6 faces com cores uniformes).
* **Mapeamento no Código:** Implementado em `problems/cubo_problem.py` no método `goal_test(self, state)`, que compara o estado atual com o `ESTADO_INICIAL` de referência.

### ● Custo de Caminho (`path_cost`)

* **Definição:** O custo de cada movimento é unitário ($g(n) = 1$).
* **Mapeamento no Código:** Gerenciado pelo método `path_cost` herdado da classe `Problem` (AIMA), onde o custo total é a soma dos movimentos realizados até o nó atual.


---

##  Classificação do Ambiente

Segundo os critérios do AIMA, o ambiente do Cubo Mágico 2x2 é classificado como:

* **Totalmente Observável**: O agente tem acesso completo ao estado do cubo (os 24 stickers) a cada momento, sem incerteza sobre a posição das cores.
* **Determinístico**: O resultado de qualquer ação (movimento de face) é perfeitamente previsível. Não há elementos de sorte ou incerteza na transição de estados.
* **Estático**: O ambiente não se altera enquanto o agente está deliberando/calculando a solução. O cubo permanece parado até que o agente decida agir.
* **Discreto**: Existe um número finito e bem definido de estados e ações possíveis. Os movimentos são realizados em passos claros (90°).
* **Agente Único**: Apenas o algoritmo de busca atua sobre o cubo para resolvê-lo; não há adversários ou outros agentes alterando o estado simultaneamente.

---


## Instalação

### 1. Clone o repositório da aima-python

Dentro da pasta `projectGrupo1/`, execute:

```bash
git clone https://github.com/aimacode/aima-python.git
```

### 2. Instale as dependências da aima-python

```bash
cd aima-python
pip install -r requirements.txt
cd ..
```

### 3. Instale o pytest (para os testes)

```bash
pip install pytest
```

---

## Execução

### Rodar o solucionador principal

A partir da raiz do projeto:

```bash
python main.py
```

O programa embaralha o cubo com 6 movimentos e resolve usando A*.

### Rodar os testes

```bash
pytest tests/test_cubo.py -v
```

---

## Representação do Cubo

O cubo é representado como uma lista/tupla de **24 strings** (stickers):

| Índices | Face  | Cor (resolvido) |
|---------|-------|-----------------|
| 0–3     | DOWN  | branco (w)      |
| 4–7     | LEFT  | laranja (o)     |
| 8–11    | BACK  | verde (g)       |
| 12–15   | UP    | amarelo (y)     |
| 16–19   | RIGHT | vermelho (r)    |
| 20–23   | FRONT | azul (b)        |

Dentro de cada face, vista de frente: índice 0 = baixo-esq, 1 = cima-esq, 2 = cima-dir, 3 = baixo-dir.

---

## Movimentos

12 movimentos: 6 faces × 2 direções (CW = horário, CCW = anti-horário)

```
('DOWN', 'CW'), ('DOWN', 'CCW'),
('LEFT', 'CW'), ('LEFT', 'CCW'),
('BACK', 'CW'), ('BACK', 'CCW'),
('UP',   'CW'), ('UP',   'CCW'),
('RIGHT','CW'), ('RIGHT','CCW'),
('FRONT','CW'), ('FRONT','CCW')
```

---

## Heurísticas e Algoritmos Implementados

O projeto utiliza a base sólida da biblioteca `aima-python`, aplicando o conceito de **herança e especialização** para resolver as particularidades do Cubo Mágico 2x2.

### ● Visão Geral do Algoritmo

* **A*** com $f(n) = g(n) + h(n)$.
* **Heurística $h$**: Baseada na contagem de faces com cores mistas, dividida por 4 para manter a admissibilidade.
* **Canonicalização**: Estados equivalentes por rotação do cubo são tratados como idênticos, reduzindo o espaço de busca em até 24×.

### ● Detalhamento das Heurísticas

Definimos duas funções no arquivo `agents/cubo_agent.py`:

1. **Heurística Principal (`h`)**:
* **Definição**: h(n) = ceil( (soma das cores_extras) / 4 )
* **Intuição**: Como cada movimento de face altera exatamente 4 stickers simultaneamente, contamos quantos stickers estão fora da cor predominante de sua face e dividimos pelo potencial máximo de correção de um único movimento.
* **Admissibilidade**: É **admissível**, pois nunca superestima o custo real; o cubo não pode ser resolvido com menos movimentos do que o necessário para organizar esses stickers individualmente.
* **Impacto**: Reduz drasticamente o número de nós expandidos em relação à busca cega (BFS).


2. **Heurística Alternativa (`h2`)**:
* **Definição**: h2(n) = (soma das cores_extras) / 4
* **Justificativa**: Versão utilizando divisão real (sem o arredondamento para cima), utilizada para analisar o impacto de uma heurística levemente menos "informada" no desempenho do agente.



### ● Adaptação das Estruturas AIMA (Justificativa)

Conforme a especificação do projeto, o grupo não reescreveu o repositório do zero, mas estendeu as classes base para suportar a **Canonicalização**:

| Estrutura Base AIMA | Subclasse / Adaptação | Justificativa Técnica |
| --- | --- | --- |
| `Problem` | `ProblemaCubo` | Implementação obrigatória da modelagem do domínio (ações, resultado e teste de objetivo). |
| `Node` | `NodeCubo` | Adição da propriedade `getCanonicalState`. No cubo, um estado possui 24 orientações físicas idênticas. Esta subclasse permite identificar estados equivalentes e evitar ciclos redundantes. |
| `best_first_graph_search` | `best_first_graph_search3` | Adaptação para que a verificação de estados repetidos (`explored set`) utilize a forma **canônica** do nó em vez do estado bruto, otimizando a busca em 24 vezes. |
| `breadth_first_graph_search` | `breadth_first_graph_search2` | Especialização da busca em largura que integra a detecção de duplicatas via canonicalização para evitar a explosão combinatória. |
| `astar_search` | `astar_search2` | Especialização que utiliza o motor de busca informada adaptado com cache de valores heurísticos para otimizar a performance. |

---

### ● Algoritmos Utilizados

* **A*** (`astar_search2`): Escolhido por ser um algoritmo de busca informada que garante a solução ótima (caminho mais curto) desde que a heurística seja admissível.
* **Busca em Largura** (`breadth_first_graph_search2`): Utilizada como base de comparação para validar a eficiência da busca informada sobre a busca cega.

### ● Algoritmos Não Utilizados (Exemplos do AIMA)

* **Busca em Profundidade (DFS)**.
* **Busca de Custo Uniforme (UCS)**.
* **Busca Gananciosa (Greedy Best-First Search)**.

### ● Justificativa de Inadequação

* **Busca em Profundidade (DFS)**: Inadequada porque o espaço de estados do cubo mágico é vasto e possui muitos ciclos. A DFS poderia mergulhar em caminhos infinitos ou encontrar soluções extremamente longas e ineficientes, não garantindo o caminho mínimo.
* **Busca de Custo Uniforme (UCS)**: Como no cubo mágico todas as ações têm custo unitário ($g(n)=1$), a UCS se comportaria exatamente como uma Busca em Largura (BFS), porém com o custo adicional de manter uma fila de prioridade sem o auxílio de uma heurística para guiar a busca.
* **Busca Gananciosa**: Embora rápida, ela ignora o custo do caminho já percorrido $g(n)$, focando apenas na estimativa futura $h(n)$. Isso faria com que o agente encontrasse soluções rapidamente, mas que não seriam as melhores (mínimo de movimentos), o que é um requisito importante para o Cubo Mágico.

---
