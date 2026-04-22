# ui/headers.py
# Header and rule functions

from fsf.ui.styles import C, G, R, W, Y, HEAD


def header(title=""):
    if title:
        print(f"{C} \u250c\u2500 {HEAD} {R}{W}formseal-fetch{R}  {Y}{title}{R}")
    else:
        print(f"{C} \u250c\u2500 {HEAD} {R}{W}formseal-fetch{R}")
    print(G + " " + "\u2500" * 52 + R)


def rule():
    print(G + " " + "\u2500" * 52 + R)