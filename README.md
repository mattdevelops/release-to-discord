## GitHub Release/Tag to Discord webhook

Python program that looks up and refreshes the GitHub Atom feed or polls the GitHub API which grabs data that is posted to a Discord webhook with great customisation.
Recommended to be run on a ([Ubuntu](https://ubuntu.com/download/server)) server using a process manager ([PM2](https://www.npmjs.com/package/pm2) recommended). You could also use a cloud platform service (PaaS) to run the code such as [Heroku](https://www.heroku.com/).

### Setup (using a server)
1. Ensure you have [Python 3](https://www.python.org/downloads/) installed on your server of choice
2. Install the requirements for this package using `pip install -r requirements.txt`
3. Copy `feeds/default.json` to `feeds/<config_name>.json` and add the appropriate blank values
4. Using your process manager, setup main.py to run. I recommend using PM2 so it would be `pm2 start main.py --name=release-to-discord --interpreter=python3`
5. Complete! Every time the Atom feed/API updates, the latest post will be sent to the Discord webhook

### Example usage
I use this program to get the dependency updates for various packages I use.