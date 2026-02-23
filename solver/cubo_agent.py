"""
cubo_agent.py
-------------
Agente solucionador do cubo mágico 2x2.

Contém:
  - NodeCubo: nó de busca com canonicalização por rotação.
  - h: heurística admissível baseada em faces incorretas.
  - best_first_graph_search3: busca best-first com detecção de estados duplicados
    usando forma canônica.
  - astar_search2: A* usando best_first_graph_search3.
  - breadth_first_graph_search2: BFS com NodeCubo.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'aima-python'))

from collections import deque
from search import Node, PriorityQueue, memoize
from env.cube_env import SIDES, INDICES
from env.canonicalize import canonical_fast


# ── Nó de busca ─────────────────────────────────────────────────────────────────
class NodeCubo(Node):
    """Nó de busca que armazena a forma canônica do estado (lazy)."""

    def __init__(self, state, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
        self._canonical = None

    def getCanonicalState(self):
        if self._canonical is None:
            self._canonical = canonical_fast(self.state)
        return self._canonical

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        return NodeCubo(
            next_state, self, action,
            problem.path_cost(self.path_cost, self.state, action, next_state)
        )


# ── Heurística ──────────────────────────────────────────────────────────────────
def h(node):
    """
    Heurística admissível: conta faces com cores mistas.
    Cada face incorreta precisa de pelo menos 1 movimento para ser corrigida,
    mas 1 movimento afeta até 4 faces → divide por 4 (arredondado para cima).
    """
    total = 0
    for side in SIDES:
        m = INDICES[side][0]
        total += len(set(node.state[m:m + 4])) - 1
    return (total + 3) // 4


# ── Algoritmos de busca ─────────────────────────────────────────────────────────
def best_first_graph_search3(problem, h_func, display=False):
    """
    Busca best-first com f(n) = g(n) + h(n), usando forma canônica para
    detectar estados equivalentes por rotação.
    """
    frontier_h = {}  # canonical -> h-value cache

    def f_with_cache(node):
        canonical = node.getCanonicalState()
        if canonical not in frontier_h:
            frontier_h[canonical] = h_func(node)
        return node.path_cost + frontier_h[canonical]

    node = NodeCubo(problem.initial)
    frontier = PriorityQueue('min', f_with_cache)
    frontier.append(node)
    explored = set()

    frontier_best = {}  # canonical -> best f-value
    frontier_node = {}  # canonical -> best node

    canonical = node.getCanonicalState()
    node_f = f_with_cache(node)
    frontier_best[canonical] = node_f
    frontier_node[canonical] = node
    frontier_h[canonical] = h_func(node)

    while frontier:
        node = frontier.pop()
        canonical = node.getCanonicalState()
        node_f = f_with_cache(node)

        if canonical in frontier_best and frontier_best[canonical] < node_f:
            continue

        frontier_best.pop(canonical, None)
        frontier_node.pop(canonical, None)

        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths expanded,", len(frontier), "paths remain")
            return node

        explored.add(canonical)

        for child in node.expand(problem):
            child_canonical = child.getCanonicalState()
            child_f = f_with_cache(child)

            if child_canonical in explored:
                continue

            if child_canonical in frontier_best:
                if child_f < frontier_best[child_canonical]:
                    frontier_best[child_canonical] = child_f
                    frontier_node[child_canonical] = child
                    frontier.append(child)
            else:
                frontier_best[child_canonical] = child_f
                frontier_node[child_canonical] = child
                frontier.append(child)

    return None


def astar_search2(problem, h=None, display=False):
    """
    A* com canonicalização por rotação.
    Requer que h seja uma heurística admissível (função de NodeCubo → int).
    """
    return best_first_graph_search3(problem, h, display)


def breadth_first_graph_search2(problem):
    """BFS usando NodeCubo (com forma canônica para evitar duplicatas)."""
    node = NodeCubo(problem.initial)
    if problem.goal_test(node.state):
        return node
    frontier = deque([node])
    explored = set()
    while frontier:
        node = frontier.popleft()
        explored.add(node.getCanonicalState())
        for child in node.expand(problem):
            child_canonical = child.getCanonicalState()
            if child_canonical not in explored:
                if problem.goal_test(child.state):
                    return child
                frontier.append(child)
                explored.add(child_canonical)
    return None
