# injectiOwOn  
vendy is a big meanie x2

# HOW TO USE
This is a rather naïve CLI installer and as such it isn't perfect yet.
That said, it might work, so try running the following commands and report back to us:  
first of all, you will need pnpm. (it MIGHT be automated in the future)  
for windows, run:  
`npm install -g pnpm`  
for linux, you will need superuser perms. if you're sane and use sudo, it should be:  
`sudo npm install -g pnpm`  
then you can just run this command and everything should be handled by us:  
`git clone https://github.com/exhq/injectiOwOn; python ./injectiOwOn/.`


# Adding platform support
Just send in a PR that adds a platform-specific file and make the proper changes
to `__main__.py`. Just ensure all of the logic happens in a function called `get_discord`
that takes one optional string argument that matches a release channel.
Look at the Windows and Linux code for reference material.  
Alternatively, let ECHO know what to add/fix in the Vencord server!
