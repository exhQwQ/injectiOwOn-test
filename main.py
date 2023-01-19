import os
from pathlib import Path

discordfolder = ""

if not os.access('/etc/shadow', os.R_OK):
    print("run with sudo bitchass")
    exit()
p = Path('.')
vencord_base_path = Path(__file__).parent.parent.absolute()
dist_path = vencord_base_path / 'dist'
if not dist_path.exists():
    print("bitchass, run \"pnpm i\" and \"pnpm build\" first")
    exit()
discord_paths = [
    "/usr/share/discord",
    "/usr/lib64/discord",
    "/opt/discord",
    Path(os.environ['HOME']) / ".local/share/discord"
]
for i in discord_paths:
    if Path(i).exists():
        discordfolder = i
with open(discordfolder+'/resources/app.asar/test.js', 'w') as f:
    filecontent = f"require('{str(dist_path.absolute())}/patcher.js')"
    f.write(filecontent)
print("done, i think")
