"""
cubo_problem.py
---------------
Subclasse de Problem (aima-python) para o cubo mágico 2x2.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'aima-python'))

from search import Problem
from env.cube_env import TURNS, SIDES, INDICES, apply_move, check


class ProblemaCubo(Problem):
    """
    Formulação do problema do cubo mágico 2x2 para busca.

    Estado: tupla de 24 strings representando os stickers.
    Ação: tupla (face, direção), ex: ('FRONT', 'CW').
    """

    def actions(self, state):
        """Retorna todos os 12 movimentos possíveis."""
        return TURNS

    def result(self, state, action):
        """Aplica a ação e retorna o novo estado."""
        return apply_move(state, action[0], action[1])

    def path_cost(self, c, state1, action, state2):
        """Custo uniforme: cada movimento custa 1."""
        return c + 1

    def goal_test(self, state):
        """O cubo está resolvido quando todas as faces têm cor uniforme."""
        return all(check(state, side) for side in SIDES)
