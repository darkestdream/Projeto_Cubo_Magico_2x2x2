"""
main.py
-------
Solucionador do cubo mágico 2x2 com visualização ASCII passo a passo.
"""

import sys
import os
import time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'aima-python'))

from env.cube_env import ESTADO_INICIAL, shuffle, apply_move
from env.display import print_cube
from problems.cubo_problem import ProblemaCubo
from solver.cubo_agent import *

DIRECTION_LABEL = {"CW": "↻ horário", "CCW": "↺ anti-horário"}


def print_solution_steps(solution):
    """Exibe o cubo após cada movimento da solução."""
    if solution is None:
        print("❌ Nenhuma solução encontrada.")
        return

    path = solution.path()
    print(f"\n✅ Solução encontrada em {solution.path_cost} movimentos!\n")
    print("─" * 40)

    print_cube(path[0].state, label="Estado inicial (embaralhado):")

    for i, node in enumerate(path[1:], 1):
        side, direction = node.action
        label = f"Movimento {i}/{solution.path_cost}: {side} {DIRECTION_LABEL[direction]}"
        print("─" * 40)
        print_cube(node.state, label=label)
        time.sleep(0.3)

    print("─" * 40)
    print("🎉 Cubo resolvido!\n")


def main():
    print("=" * 40)
    print("  Solucionador de Cubo Mágico 2x2")
    print("         Grupo 3")
    print("=" * 40)

    print_cube(tuple(ESTADO_INICIAL), label="Cubo resolvido (referência):")

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
    estado_embaralhado=shuffle(ESTADO_INICIAL,n=30)

    print("\nBuscando solução com A* com peso ...")
    problem = ProblemaCubo(estado_embaralhado)
    solution = astar_search2(problem, h=lambda n: h(n)*3, display=True)
    print_solution_steps(solution)
    
    print("\nBuscando solução com A* com peso ...h2")
    problem = ProblemaCubo(estado_embaralhado)
    solution = astar_search2(problem, h=lambda n: h2(n)*3, display=True)
    print_solution_steps(solution)
    
    print("\nBuscando solução com A*...")
    problem = ProblemaCubo(estado_embaralhado)
    solution = astar_search2(problem, h=h, display=True)
    print_solution_steps(solution)
    
    print("\nBuscando solução com A*...h2")
    problem = ProblemaCubo(estado_embaralhado)
    solution = astar_search2(problem, h=h2, display=True)
    
    print_solution_steps(solution)
    print("\nBuscando solução com breadth-first..")
    problem = ProblemaCubo(estado_embaralhado)
    solution = breadth_first_graph_search2(problem, display=True)

    print_solution_steps(solution)
    
    


if __name__ == "__main__":
    main()
