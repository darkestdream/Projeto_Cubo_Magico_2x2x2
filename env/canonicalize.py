"""
canonicalize.py
---------------
Funções para obter a forma canônica de um estado do cubo, removendo
equivalências por rotação.
"""

from copy import deepcopy
from .cube_env import CubeRotate, ESTADO_INICIAL

# ── Gera as 24 rotações do cubo ─────────────────────────────────────────────────
_ROTATIONS_1 = [
    lambda c: c,
    lambda c: c.rotate_clockwise_left(),
    lambda c: c.rotate_clockwise_left().rotate_clockwise_left(),
    lambda c: c.rotate_clockwise_left().rotate_clockwise_left().rotate_clockwise_left(),
    lambda c: c.rotate_clockwise_down(),
    lambda c: c.rotate_clockwise_down().rotate_clockwise_down().rotate_clockwise_down(),
]
_ROTATIONS_2 = [
    lambda c: c,
    lambda c: c.rotate_clockwise_back(),
    lambda c: c.rotate_clockwise_back().rotate_clockwise_back(),
    lambda c: c.rotate_clockwise_back().rotate_clockwise_back().rotate_clockwise_back(),
]

ROTATIONS = []
for _i in _ROTATIONS_1:
    for _j in _ROTATIONS_2:
        ROTATIONS.append(lambda c, i=_i, j=_j: j(i(c)))

ROTATION_PERMUTATIONS = {i: ROTATIONS[i](CubeRotate()).state for i in range(24)}

def _get_inverse_rotation(rot_idx):
    cube = ROTATIONS[rot_idx](CubeRotate())
    for j in range(24):
        if ROTATIONS[j](cube).state == CubeRotate().state:
            return j
    return 0

INVERSE_ROTATION = {i: _get_inverse_rotation(i) for i in range(24)}

# Mapeamento canto → rotação canônica
_solved = tuple(ESTADO_INICIAL)
_rot_idx_to_corner = {}
for _i in range(24):
    _perm = ROTATION_PERMUTATIONS[_i]
    _rotated = tuple(_solved[_perm[k]] for k in range(24))
    _rot_idx_to_corner[_i] = (_rotated[0], _rotated[4], _rotated[8])

_corner_to_rot_idx = {v: k for k, v in _rot_idx_to_corner.items()}
corner_to_canonical_rotation = {
    corner: INVERSE_ROTATION[rot_idx]
    for corner, rot_idx in _corner_to_rot_idx.items()
}


def canonical_fast(state):
    """
    Retorna a forma canônica do estado, normalizando por rotações do cubo.
    Escolhe a tupla lexicograficamente menor entre as 24 rotações possíveis,
    usando o canto dominante para podar candidatos.
    """
    best = None
    best_corner = None
    candidates = []

    for r in range(24):
        perm = ROTATION_PERMUTATIONS[r]
        c = (state[perm[0]], state[perm[4]], state[perm[8]])
        if best_corner is None or c < best_corner:
            best_corner = c
            candidates = [r]
        elif c == best_corner:
            candidates.append(r)

    for r in candidates:
        perm = ROTATION_PERMUTATIONS[r]
        rotated = tuple(state[perm[i]] for i in range(24))
        if best is None or rotated < best:
            best = rotated

    return best


def apply_rotation_to_state(state, rot_idx):
    """Aplica a rotação rot_idx a um estado."""
    perm = ROTATION_PERMUTATIONS[rot_idx]
    return tuple(state[perm[i]] for i in range(24))
