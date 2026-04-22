# fsf/general/errors.py
# Error handlers

from fsf.ui import fail, br


def unknown_command(cmd):
    br()
    fail(f"Unknown command: {cmd}\nRun 'fsf --help' for available commands")


def command_not_implemented(cmd):
    br()
    fail(f"Command not implemented: {cmd}")


def handle_interrupt():
    from fsf.ui import br, info
    br()
    info("Interrupted.")
    br()


def handle_exception(e):
    from fsf.ui import fail
    fail(str(e))