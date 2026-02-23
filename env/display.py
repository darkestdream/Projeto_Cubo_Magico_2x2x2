"""
display.py
----------
Exibe o cubo 2x2 como um mapa 2D em ASCII no terminal, com cores ANSI.

Layout do mapa (unfolded net):

        [ UP  ]
[ LEFT ][ FRONT ][ RIGHT ][ BACK ]
        [ DOWN]

Cada face tem 2x2 stickers.
"""

# ── Cores ANSI ──────────────────────────────────────────────────────────────────
ANSI = {
    'w': '\033[97m',   # branco
    'y': '\033[93m',   # amarelo
    'r': '\033[91m',   # vermelho
    'o': '\033[38;5;208m',  # laranja
    'b': '\033[94m',   # azul
    'g': '\033[92m',   # verde
}
RESET = '\033[0m'
BOLD  = '\033[1m'

COLOR_NAMES = {
    'w': 'White',
    'y': 'Yellow',
    'r': 'Red',
    'o': 'Orange',
    'b': 'Blue',
    'g': 'Green',
}

def _colored(char):
    color = ANSI.get(char, '')
    return f"{BOLD}{color}▓▓{RESET}"

def _face(state, start):
    """Retorna os 4 stickers de uma face como grid 2x2.
    Índices: 0=baixo-esq, 1=cima-esq, 2=cima-dir, 3=baixo-dir
    """
    s = state[start:start+4]
    # linha de cima: [1, 2], linha de baixo: [0, 3]
    top = [s[1], s[2]]
    bot = [s[0], s[3]]
    return top, bot

def print_cube(state, label=None):
    """Imprime o cubo como mapa 2D ASCII com cores."""
    if label:
        print(f"\n{BOLD}{label}{RESET}")

    # Extrair faces
    # DOWN=0, LEFT=4, BACK=8, UP=12, RIGHT=16, FRONT=20
    up_t,  up_b  = _face(state, 12)
    lf_t,  lf_b  = _face(state, 4)
    fr_t,  fr_b  = _face(state, 20)
    rt_t,  rt_b  = _face(state, 16)
    bk_t,  bk_b  = _face(state, 8)
    dn_t,  dn_b  = _face(state, 0)

    gap = "      "  # 6 spaces to align with face width (each sticker = 2 chars)

    lines = [
        # UP face (centered above FRONT)
        f"{gap}┌────┐",
        f"{gap}│{''.join(_colored(c) for c in up_t)}│",
        f"{gap}│{''.join(_colored(c) for c in up_b)}│",
        f"{gap}└────┘",
        # Middle row: LEFT FRONT RIGHT BACK
        f"┌────┬────┬────┬────┐",
        f"│{''.join(_colored(c) for c in lf_t)}│{''.join(_colored(c) for c in fr_t)}│{''.join(_colored(c) for c in rt_t)}│{''.join(_colored(c) for c in bk_t)}│",
        f"│{''.join(_colored(c) for c in lf_b)}│{''.join(_colored(c) for c in fr_b)}│{''.join(_colored(c) for c in rt_b)}│{''.join(_colored(c) for c in bk_b)}│",
        f"└────┴────┴────┴────┘",
        # DOWN face
        f"{gap}┌────┐",
        f"{gap}│{''.join(_colored(c) for c in dn_t)}│",
        f"{gap}│{''.join(_colored(c) for c in dn_b)}│",
        f"{gap}└────┘",
    ]

    # Face labels
    face_labels = ["  UP  ", " LEFT ", "FRONT ", "RIGHT ", " BACK ", " DOWN "]

    print(f"{gap}  UP")
    for line in lines[:4]:
        print(line)
    print("LEFT  FRONT RIGHT  BACK")
    for line in lines[4:8]:
        print(line)
    print(f"{gap}  DOWN")
    for line in lines[8:]:
        print(line)
    print()
