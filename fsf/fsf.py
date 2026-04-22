# Main entry point

import sys
import os
from pathlib import Path

script_dir = Path(__file__).absolute()
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))
os.chdir(project_root)

from fsf.cmd import COMMANDS
from fsf.general.aliases import resolve
from fsf.general.errors import unknown_command, handle_interrupt, handle_exception

from fsf.commands.general import about as cmd_about
from fsf.commands.general import version as cmd_version
from fsf.commands.general import help as cmd_help


def main():
    if len(sys.argv) < 2:
        cmd_about.run()
        return

    args = resolve(sys.argv[1:])
    cmd = args[0].lower()
    cmd_args = args[1:]

    if cmd == "--help":
        cmd_help.run()
        return

    if cmd == "--about":
        cmd_about.run()
        return

    if cmd == "version" or cmd == "--version":
        cmd_version.run()
        return

    if cmd == "--aliases":
        cmd_help.run_aliases()
        return

    if cmd not in COMMANDS:
        unknown_command(cmd)

    _, handler = COMMANDS[cmd]

    try:
        handler(cmd_args)
    except KeyboardInterrupt:
        handle_interrupt()
        sys.exit(130)
    except Exception as e:
        handle_exception(e)


if __name__ == "__main__":
    main()