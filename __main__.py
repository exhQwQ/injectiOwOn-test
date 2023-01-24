#!/usr/bin/env python3

import os
from pathlib import Path
import argparse
import errno
import subprocess
import sys
import requests
import zipfile


if "linux" in sys.platform:
    from linux import get_discord
elif "win" in sys.platform:
    from windows import get_discord
else:
    print(f"Sorry, {sys.platform} is not yet supported!")
    exit(1)

parser = argparse.ArgumentParser(
    prog="InjectiOwOn",
    description=("Makes a piss poor attempt at being a CLI Vencord installer, "
                 "but doesn't do so in the Devil's tongue (Go)"),
    epilog="Proudly presented by ECHO & Riven Skaye"
)
parser.add_argument(
    "channel",
    default="stable",
    choices=["stable", "canary", "dev", "devel", "development", "ptb"],
    type=str.lower,
    help="Optional release channel to install for."
)

# @ECHO please do add a short and long option pair for people to specify a
# custom path. It should point to the resources folder. Symlinks and
# relative paths should be safe, so you'll need to edit some code to handle it.
# parser.add_argument("-p", "--installdir", ...)


def main() -> None:
    if "linux" in sys.platform and not os.geteuid() == 0:
        print("please run with superuser perms :3")
        exit(1)
    print("welcome to InjectiOwOn! Sit back and I'll do everything :3")


    print("downloading vencord.....")
    url = 'https://codeload.github.com/Vendicated/Vencord/zip/refs/heads/main'
    r = requests.get(url, allow_redirects=True)
    print("extracting.....")
    open('base.zip', 'wb').write(r.content)
    with zipfile.ZipFile("./base.zip", 'r') as zip_ref:
        zip_ref.extractall(".")
    print("installing needed packages")
    os.chdir("./Vencord-main")
    os.system("pnpm i; pnpm build")
    

#now we can use our own vencord

    discordfolder: Path = Path(".")
    vencord_base_path = Path(__file__).parent/"Vencord-main"

    dist_path = vencord_base_path / "dist"
    if not dist_path.exists():
        print("bitchass, run `pnpm i` and `pnpm build` first")
        exit()

    try:
        discordfolder = get_discord(args.channel)
    except FileNotFoundError as fnfe:
        print(f"{fnfe.strerror}\n{fnfe.errno}: {os.strerror(fnfe.errno)}")

    for child in discordfolder.iterdir():
        if child.name.lower() == "resources":
            discordfolder = child
            break
        elif child.name.lower().startswith("app-"):
            for grandchild in child.iterdir():
                if grandchild.name.lower() == "resources":
                    discordfolder = grandchild
                    break
        elif child.name.startswith("Discord"):
            for grandchild in child.iterdir():
                if grandchild.name.lower() == "resources":
                    discordfolder = grandchild
                    break
                elif child.name.lower().startswith("app-"):
                    for greatgrandchild in child.iterdir():
                        if greatgrandchild.name.lower() == "resources":
                            discordfolder = greatgrandchild
                            break
    else:
        raise OSError(errno.ENOENT,
                      "Proper folder not found, please start Discord once!",
                      str(discordfolder))

    (discordfolder / "app").mkdir(parents=False, exist_ok=True)
    appfolder = discordfolder/"app"
    (appfolder/"package.json").touch(exist_ok=True)
    (appfolder/"index.js").touch(exist_ok=True)

    with open(appfolder/"package.json", "w+") as pkg:
        pkg.write('{ "name": "discord", "main": "index.js" }\n')
    with open(appfolder/"index.js", "w+") as idx:
        idx.write(f"require({dist_path/'patcher.js'});\n"
                  "require(../app.asar);")

    print("That should be all. Please fully close Discord and restart to check"
          " if it worked, your settings should contain a Vencord listing!")


args = parser.parse_args()
if __name__ == "__main__":
    main()
