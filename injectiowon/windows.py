from pathlib import Path
from typing import Optional
import errno
import os


def get_discord(channel: str = "stable") -> Path:
    cname = ""
    discordfolder: Optional[Path] = None
    channel = channel.lower()
    if channel == "ptb":
        cname = "PTB"
    elif channel == "canary":
        cname = "Canary"
    elif "dev" in channel:
        cname = "Development"

    # This should always produce a result except for a handful of edgecases
    # e.g. when users manage to unset the envvar, when they run as a diff user
    # or if they manage to call this from a recovery shell.
    # Possibly through some safe mode configs as well.
    LAD = os.getenv("LocalAppData")
    discordfolder = Path(LAD) / f"Discord{cname}" if LAD is not None else None

    if discordfolder is None or not discordfolder.exists():
        raise OSError(errno.ENOENT,
                      "Discord path not found! Please see the README "
                      "about supported paths and installation methods.",
                      f"{LAD}/{f'Discord{cname}'}")

    return discordfolder / f"Discord{cname}"
