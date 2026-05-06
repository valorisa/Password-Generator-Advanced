"""Copie dans le presse-papier (cross-platform, stdlib uniquement)."""

import subprocess
import sys


def copy_to_clipboard(text: str) -> bool:
    try:
        if sys.platform == "win32":
            process = subprocess.Popen(
                ["clip"], stdin=subprocess.PIPE, shell=True
            )
            process.communicate(text.encode("utf-16le"))
        elif sys.platform == "darwin":
            process = subprocess.Popen(
                ["pbcopy"], stdin=subprocess.PIPE
            )
            process.communicate(text.encode("utf-8"))
        else:
            process = subprocess.Popen(
                ["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE
            )
            process.communicate(text.encode("utf-8"))
        return process.returncode == 0
    except (OSError, FileNotFoundError):
        return False
