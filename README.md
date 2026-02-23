# Cubo Mágico 2x2 — Grupo 1

Solucionador do cubo mágico 2×2 usando busca A* com canonicalização por rotação, implementado sobre a biblioteca [aima-python](https://github.com/aimacode/aima-python).

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
