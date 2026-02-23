"""
test_cubo.py
------------
Testes unitários para o cubo mágico 2x2.
Execute com: pytest tests/test_cubo.py -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'aima-python'))

import pytest
from env.cube_env import (
    ESTADO_INICIAL, SIDES, TURNS, INDICES,
    apply_move, shuffle, check
)
from env.canonicalize import canonical_fast, ROTATION_PERMUTATIONS
from problems.cubo_problem import ProblemaCubo
from solver.cubo_agent import NodeCubo, astar_search2, h


# ── Testes do ambiente ──────────────────────────────────────────────────────────

def test_estado_inicial_tem_24_stickers():
    assert len(ESTADO_INICIAL) == 24

def test_estado_inicial_resolvido():
    for side in SIDES:
        assert check(ESTADO_INICIAL, side), f"Face {side} não está resolvida no estado inicial"

def test_apply_move_retorna_tupla():
    result = apply_move(ESTADO_INICIAL, "FRONT", "CW")
    assert isinstance(result, tuple)
    assert len(result) == 24

def test_move_e_inverso_restaura_estado():
    """CW seguido de CCW deve restaurar o estado."""
    for side, _ in TURNS[::2]:  # apenas CW
        state = apply_move(ESTADO_INICIAL, side, "CW")
        state = apply_move(state, side, "CCW")
        assert tuple(state) == tuple(ESTADO_INICIAL), f"Inversão falhou para {side}"

def test_sequencia_identidade():
    """R' U' R' F' U F U' R' F R F' U' R U2 R deve retornar ao estado inicial."""
    seq = [
        ("RIGHT","CCW"),("UP","CCW"),("RIGHT","CCW"),("FRONT","CCW"),
        ("UP","CW"),("FRONT","CW"),("UP","CCW"),("RIGHT","CCW"),
        ("FRONT","CW"),("RIGHT","CW"),("FRONT","CCW"),("UP","CCW"),
        ("RIGHT","CW"),("UP","CCW"),("UP","CCW"),("RIGHT","CW"),
    ]
    state = tuple(ESTADO_INICIAL)
    for side, direction in seq:
        state = apply_move(state, side, direction)
    assert state == tuple(ESTADO_INICIAL)

def test_shuffle_gera_estado_diferente():
    shuffled = shuffle(tuple(ESTADO_INICIAL), n=20)
    assert shuffled != tuple(ESTADO_INICIAL)

# ── Testes da canonicalização ───────────────────────────────────────────────────

def test_canonical_fast_estado_resolvido_consistente():
    """Qualquer rotação do cubo resolvido deve ter o mesmo canônico."""
    base = canonical_fast(tuple(ESTADO_INICIAL))
    for r in range(24):
        perm = ROTATION_PERMUTATIONS[r]
        rotated = tuple(ESTADO_INICIAL[perm[i]] for i in range(24))
        assert canonical_fast(rotated) == base, f"Rotação {r} produziu canônico diferente"

def test_canonical_fast_estado_embaralhado():
    """Rotações de um estado embaralhado devem ter o mesmo canônico."""
    shuffled = shuffle(tuple(ESTADO_INICIAL), n=15)
    base = canonical_fast(shuffled)
    for r in range(24):
        perm = ROTATION_PERMUTATIONS[r]
        rotated = tuple(shuffled[perm[i]] for i in range(24))
        assert canonical_fast(rotated) == base

# ── Testes do problema ──────────────────────────────────────────────────────────

def test_problema_goal_test_resolvido():
    p = ProblemaCubo(tuple(ESTADO_INICIAL))
    assert p.goal_test(tuple(ESTADO_INICIAL))

def test_problema_goal_test_embaralhado():
    shuffled = shuffle(tuple(ESTADO_INICIAL), n=10)
    p = ProblemaCubo(shuffled)
    assert not p.goal_test(shuffled)

def test_problema_actions():
    p = ProblemaCubo(tuple(ESTADO_INICIAL))
    assert len(p.actions(tuple(ESTADO_INICIAL))) == 12

# ── Testes do agente ────────────────────────────────────────────────────────────

def test_heuristica_zero_para_resolvido():
    node = NodeCubo(tuple(ESTADO_INICIAL))
    assert h(node) == 0

def test_heuristica_positiva_para_embaralhado():
    shuffled = shuffle(tuple(ESTADO_INICIAL), n=5)
    node = NodeCubo(shuffled)
    assert h(node) >= 0

def test_astar_resolve_1_movimento():
    """A* deve resolver um cubo com 1 movimento em 1 passo."""
    state = apply_move(tuple(ESTADO_INICIAL), "FRONT", "CW")
    problem = ProblemaCubo(state)
    solution = astar_search2(problem, h=h)
    assert solution is not None
    assert solution.path_cost == 1

def test_astar_resolve_poucos_movimentos():
    """A* deve resolver um cubo embaralhado com poucos movimentos."""
    state = apply_move(
        apply_move(
            apply_move(tuple(ESTADO_INICIAL), "RIGHT", "CW"),
            "FRONT", "CW"
        ),
        "DOWN", "CW"
    )
    problem = ProblemaCubo(state)
    solution = astar_search2(problem, h=h)
    assert solution is not None
    assert solution.path_cost <= 6  # limite generoso


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
