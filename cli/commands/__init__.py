from pathlib import Path

VERSION_PATH = Path(__file__).parent.parent.parent / "version.txt"


def get_version():
    try:
        return VERSION_PATH.read_text(encoding="utf-8").strip()
    except:
        return "dev"


VERSION = get_version()
