from pathlib import Path
from typing import List, Optional
import errno
import os


def get_discord(channel: str = "stable") -> Path:
    # Package names are lowercase (discord, discord-canary, discord-ptb)
    cname = "" if channel.lower() == "stable" else f"{channel.lower()}"
    if cname == "dev" or cname == "devel":
        cname = "developer"
    altcname = (
        "Canary" if cname == "canary"
        else "PTB" if cname == "ptb"
        else "Developer"
    )
    discordfolder: Optional[Path] = None
    # This is platform specific and only runs on Unix/not Emscripten/not WASI
    if not os.geteuid() == 0:  # type: ignore
        print("run with super user perms bitchass")
        exit()

    discord_paths: List[str] = [
        f"/usr/share/discord-{cname}",
        f"/usr/lib64/discord-{cname}",
        f"/opt/discord-{cname}",
        f"{os.environ['HOME']}/.local/share/discord-{cname}"
        f"/usr/share/Discord{altcname}",
        f"/usr/lib64/Discord{altcname}",
        f"/opt/discord-{cname}",
        f"{os.environ['HOME']}/.local/share/Discord{altcname}"
    ]
    for i in discord_paths:
        with Path(i) as pi:
            if pi.exists():
                discordfolder = pi

    if discordfolder is None:
        raise OSError(errno.ENOENT,
                      "Discord path not found! Please see the README "
                      "about supported paths and installation methods.",
                      "/[usr/(share, lib64), opt]/discord")
    return discordfolder
