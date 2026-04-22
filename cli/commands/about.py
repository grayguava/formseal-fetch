# commands/about.py
# About command - shows project info

from cli.ui import br, header, C, G, W, R


def run():
    br()
    header()
    br()
    print(f"  {W}CLI for fetching encrypted form submissions{R}")
    br()
    print(f"  Part of the {C}formseal{R} ecosystem")
    br()
    print(f"  {G}License:      {R}  MIT")
    print(f"  {G}Maintained by:{R}  grayguava")
    print(f"  {G}Repository:   {R}  https://github.com/grayguava/formseal-fetch")
    br()
