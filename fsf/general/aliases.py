# fsf/general/aliases.py
# Shorthand aliases

ALIASES = {
    "-s": "status",
    "-pl": "providers",
    "-c": "connect",
    "-o": ["fetch", "--output"],
}


def resolve(args):
    """Resolve aliases in argument list."""
    if not args:
        return args

    resolved = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg in ALIASES:
            replacement = ALIASES[arg]
            if isinstance(replacement, list):
                resolved.extend(replacement)
            else:
                resolved.append(replacement)
        else:
            resolved.append(arg)
        i += 1

    return resolved