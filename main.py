"""
main.py
-------
Ponto de entrada do projeto: embaralha o cubo e resolve com A*.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'aima-python'))

from env.cube_env import ESTADO_INICIAL, shuffle, apply_move, SIDES, INDICES
from problems.cubo_problem import ProblemaCubo
from solver.cubo_agent import astar_search2, h


def print_solution(node):
    """Imprime o caminho da solução."""
    if node is None:
        print("Nenhuma solução encontrada.")
        return
    path = node.path()
    print(f"\n✅ Solução encontrada em {node.path_cost} movimentos:")
    for i, n in enumerate(path[1:], 1):
        side, direction = n.action
        print(f"  {i}. {side} {direction}")


def main():
    print("=" * 50)
    print("   Solucionador de Cubo Mágico 2x2 — Grupo 1")
    print("=" * 50)

    # Embaralha com 6 movimentos (acessível ao A*)
    estado_embaralhado = apply_move(
        apply_move(
            apply_move(
                apply_move(
                    apply_move(
                        apply_move(tuple(ESTADO_INICIAL), "RIGHT", "CW"),
                        "FRONT", "CW"),
                    "DOWN", "CW"),
                "UP", "CW"),
            "BACK", "CCW"),
        "FRONT", "CW")

    print("\nEstado inicial (resolvido):")
    print(" ", ESTADO_INICIAL)

    print("\nEstado embaralhado (6 movimentos):")
    print(" ", estado_embaralhado)

    print("\nBuscando solução com A*...")
    problem = ProblemaCubo(estado_embaralhado)
    solution = astar_search2(problem, h=h, display=True)
    print_solution(solution)


if __name__ == "__main__":
    main()
