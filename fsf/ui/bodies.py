# ui/bodies.py
# Body output functions

from fsf.ui.styles import C, D, G, O, R, S, W, Y, BOLD, RED


def br():
    print()


def badge(label, color):
    return f"{color}{BOLD} {label} {R}"


def fail(msg):
    br()
    print(f"{badge('❌', RED)} {msg}")
    br()
    raise SystemExit(1)


def row(icon, label, value):
    pad   = 12
    label = (label + " " * pad)[:pad]
    print(f"{S}{icon}{R}  {D}{label}{R}  {W}{value}{R}")


def cmd_line(command, desc):
    pad     = 34
    command = (command + " " * pad)[:pad]
    print(f"  {W}{command}{R}{G}{desc}{R}")


def code(msg):
    print(f"  {O}{msg}{R}")


def link(msg):
    print(f"  {O}{msg}{R}")


def ok(msg):
    print(f"  {G}✨{R} {msg}")


def info(msg):
    print(f"  {O}{msg}{R}")


def warn(msg):
    print(f"{Y}⚠️ {R}{msg}")