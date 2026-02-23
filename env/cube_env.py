"""
cube_env.py
-----------
Define o estado do cubo mágico 2x2, as permutações de movimentos e funções auxiliares.

Representação:
  - O cubo é uma lista de 24 stickers.
  - Índices 0-3: DOWN (branco), 4-7: LEFT (laranja), 8-11: BACK (verde),
    12-15: UP (amarelo), 16-19: RIGHT (vermelho), 20-23: FRONT (azul).
  - Dentro de cada face (vista de frente): índice 0=baixo-esq, 1=cima-esq,
    2=cima-dir, 3=baixo-dir.
  - Cores: w=branco, y=amarelo, r=vermelho, o=laranja, b=azul, g=verde
"""

import random
from copy import deepcopy

# ── Estado inicial (cubo resolvido) ────────────────────────────────────────────
DOWN  = ["w"] * 4
LEFT  = ["o"] * 4
BACK  = ["g"] * 4
UP    = ["y"] * 4
RIGHT = ["r"] * 4
FRONT = ["b"] * 4

ESTADO_INICIAL = DOWN + LEFT + BACK + UP + RIGHT + FRONT

CANONICAL_CUBE = list(range(24))

SIDES      = ["DOWN", "LEFT", "BACK", "UP", "RIGHT", "FRONT"]
DIRECTIONS = ["CW", "CCW"]
TURNS      = [(s, d) for s in SIDES for d in DIRECTIONS]

INDICES = {
    "DOWN":  list(range(0,  4)),
    "LEFT":  list(range(4,  8)),
    "BACK":  list(range(8,  12)),
    "UP":    list(range(12, 16)),
    "RIGHT": list(range(16, 20)),
    "FRONT": list(range(20, 24)),
}

# ── Rotações de face ────────────────────────────────────────────────────────────
def rotate_clockwise(side):
    """Gira CW para DOWN/BACK/LEFT; CCW para UP/FRONT/RIGHT."""
    return [side[3], side[0], side[1], side[2]]

def rotate_counterclockwise(side):
    """Gira CCW para DOWN/BACK/LEFT; CW para UP/FRONT/RIGHT."""
    return [side[1], side[2], side[3], side[0]]

# ── Classe auxiliar para calcular permutações de rotação global ─────────────────
class CubeRotate:
    def __init__(self, state=None):
        self.state = state if state is not None else list(range(24))
        self.faces = {
            "DOWN":  self.state[0:4],
            "LEFT":  self.state[4:8],
            "BACK":  self.state[8:12],
            "UP":    self.state[12:16],
            "RIGHT": self.state[16:20],
            "FRONT": self.state[20:24],
        }

    def _rebuild(self, new_face):
        new_state = (new_face["DOWN"] + new_face["LEFT"] + new_face["BACK"] +
                     new_face["UP"]   + new_face["RIGHT"]+ new_face["FRONT"])
        return CubeRotate(new_state)

    def rotate_clockwise_back(self):
        f = deepcopy(self.faces)
        f["BACK"]  = rotate_clockwise(self.faces["BACK"])
        f["FRONT"] = rotate_clockwise(self.faces["FRONT"])
        f["DOWN"]  = rotate_counterclockwise(self.faces["LEFT"])
        f["LEFT"]  = rotate_counterclockwise(self.faces["UP"][::-1])
        f["UP"]    = rotate_counterclockwise(self.faces["RIGHT"])
        f["RIGHT"] = rotate_counterclockwise(self.faces["DOWN"][::-1])
        return self._rebuild(f)

    def rotate_clockwise_left(self):
        f = deepcopy(self.faces)
        f["LEFT"]  = rotate_clockwise(self.faces["LEFT"])
        f["RIGHT"] = rotate_clockwise(self.faces["RIGHT"])
        f["DOWN"]  = rotate_counterclockwise(self.faces["FRONT"][::-1])
        f["FRONT"] = rotate_counterclockwise(self.faces["UP"])
        f["UP"]    = rotate_counterclockwise(self.faces["BACK"][::-1])
        f["BACK"]  = rotate_counterclockwise(self.faces["DOWN"])
        return self._rebuild(f)

    def rotate_clockwise_down(self):
        f = deepcopy(self.faces)
        f["DOWN"]  = rotate_clockwise(self.faces["DOWN"])
        f["UP"]    = rotate_clockwise(self.faces["UP"])
        f["RIGHT"] = rotate_counterclockwise(self.faces["FRONT"])
        f["FRONT"] = rotate_counterclockwise(self.faces["LEFT"][::-1])
        f["LEFT"]  = rotate_counterclockwise(self.faces["BACK"])
        f["BACK"]  = rotate_counterclockwise(self.faces["RIGHT"][::-1])
        return self._rebuild(f)

    def adjacent_stickers_to_front(self):
        l = [self.faces["LEFT"][3],  self.faces["LEFT"][2]]
        u = [self.faces["UP"][3],    self.faces["UP"][0]]
        r = [self.faces["RIGHT"][0], self.faces["RIGHT"][1]]
        d = [self.faces["DOWN"][2],  self.faces["DOWN"][1]]
        return l + u + r + d

# ── Stickers adjacentes (calculados uma vez) ────────────────────────────────────
ADJACENT_STICKER_INDICES = {
    "DOWN":  [22, 23, 17, 18,  9,  8,  4,  7],
    "UP":    [20, 21,  6,  5, 11, 10, 19, 16],
    "FRONT": [15, 12, 16, 17,  2,  1,  7,  6],
    "BACK":  [ 5,  4,  0,  3, 18, 19, 13, 14],
    "LEFT":  [ 1,  0,  8, 11, 14, 15, 21, 22],
    "RIGHT": [23, 20, 12, 13, 10,  9,  3,  2],
}

def _rotate_adjacent_stickers_clockwise(stickers):
    ls = list(range(24))
    for i, k in enumerate(stickers):
        ls[stickers[(i + 2) % len(stickers)]] = k
    return ls

def _full_rotate_side_clockwise(side):
    old_idx = INDICES[side]
    rotate = (rotate_counterclockwise if side in {"DOWN", "BACK", "LEFT"}
              else rotate_clockwise)
    new_idx = rotate(old_idx)
    ls = _rotate_adjacent_stickers_clockwise(ADJACENT_STICKER_INDICES[side])
    for i, k in enumerate(new_idx):
        ls[k] = old_idx[i]
    return ls

def _inverse(permutation):
    ls = [0] * 24
    for i, k in enumerate(permutation):
        ls[k] = i
    return ls

PERMUTATIONS = {
    turn: (_full_rotate_side_clockwise(turn[0]) if turn[1] == "CW"
           else _inverse(_full_rotate_side_clockwise(turn[0])))
    for turn in TURNS
}

# ── API pública ─────────────────────────────────────────────────────────────────
def apply_move(state, side, direction):
    """Aplica um movimento ao estado e retorna o novo estado como tupla."""
    perm_map = PERMUTATIONS[(side, direction)]
    return tuple(state[perm_map[i]] for i in range(24))

def shuffle(state, n=100):
    """Embaralha o estado com n movimentos aleatórios."""
    new_state = tuple(state)
    for _ in range(n):
        side, direction = random.choice(TURNS)
        new_state = apply_move(new_state, side, direction)
    return new_state

def check(state, side):
    """Verifica se todos os stickers de uma face têm a mesma cor."""
    m = INDICES[side][0]
    return len(set(state[m:m + 4])) == 1
