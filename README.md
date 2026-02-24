# Cubo Mágico 2x2 — Grupo 3

Solucionador do cubo mágico 2×2 usando busca A* com canonicalização por rotação, implementado sobre a biblioteca [aima-python](https://github.com/aimacode/aima-python).

---

## Integrantes:



---

## Estrutura do Projeto

```
.
├── aima-python/          ← dependência (clonar conforme instruções)
├── env/
│   ├── __init__.py
│   ├── cube_env.py       ← estado, movimentos, permutações
│   └── canonicalize.py   ← canonicalização por rotação do cubo
├── agents/
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

## Algoritmo

- **A\*** com `f(n) = g(n) + h(n)`
- **Heurística `h`**: conta faces com cores mistas, dividido por 4 (admissível)
- **Canonicalização**: estados equivalentes por rotação do cubo são tratados como idênticos, reduzindo o espaço de busca em até 24×

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
