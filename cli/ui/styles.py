# ui/styles.py
# All ANSI colors and styles

import os
import sys

if os.name == "nt":
    try:
        os.system("chcp 65001 >nul")
    except:
        pass

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except:
    pass

RESET  = "\x1b[0m"
BOLD   = "\x1b[1m"
DIM    = "\x1b[2m"

RED    = "\x1b[31m"
GREEN  = "\x1b[32m"
YELLOW = "\x1b[33m"
BLUE   = "\x1b[34m"
MAGENTA= "\x1b[35m"
CYAN   = "\x1b[36m"
WHITE  = "\x1b[37m"
GRAY   = "\x1b[90m"

O = "\x1b[38;5;208m"
S = "\x1b[38;5;112m"
G = "\x1b[38;5;244m"
C = "\x1b[38;5;108m"
Y = "\x1b[38;5;103m"
M = "\x1b[38;5;141m"
W = WHITE + BOLD
D = DIM
R = RESET

HEAD = "🐸"
OK = "✨"
TICK = "✔️"
CROSS = "❌"
ERR = "😵‍💫"