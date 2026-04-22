# commands/help.py
# Help command - shows all available commands

from cli.ui import br, rule, cmd_line, link, header, C, G, Y, M, W, D, R, GRAY


def run():
    from cli.fsf import HELP_GROUPS, _show_help as show_help
    show_help()


def run_aliases():
    br()
    header("shorthand aliases")
    br()

    print(f" {W}Short{R}  {G}Canonical{R}")
    print(G + " " + "\u2500" * 44 + R)
    print(f" {W}-s{R}     {G}status{R}")
    print(f" {W}-c{R}     {G}connect{R}")
    print(f" {W}-o{R}     {G}fetch --output <path>{R}")
    print(f" {W}-pl{R}    {G}providers{R}")
    br()