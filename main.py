import requests, os, json, threading, time, feedparser


try:
    open("cache.json", "r")
except:
    f = open("cache.json", "w")
    f.write("{}")
    f.close()

while True:
    # Get the full path of the folder within the current working directory
    folder_path = os.path.join(os.getcwd(), "feeds")

    # List all files in the folder
    files = os.listdir(folder_path)

    for file in files:
        if file == "default.json":
            continue
        with open(f"feeds/{file}") as config:
            config = json.load(config)

            if config['type'] == "release":
                # Make a request to the GitHub API to fetch the latest release
                url = f"https://api.github.com/repos/{config['github_repo']}/releases/latest"
                response = requests.get(url)

                # Check if the request was successful (status code 200)
                if response.status_code == 200:
                    # Get the JSON data from the response
                    release_data = response.json()

                    # Extract the name, tag name, and published date of the release
                    name = release_data["name"]
                    tag_name = release_data["tag_name"]
                    published_date = release_data["published_at"]

                    # Check cache
                    with open("cache.json", "r") as cache:
                        cache = json.load(cache)

                    if config['github_repo'] not in cache:
                        cache[config['github_repo']] = "n/a"
                    if cache[config['github_repo']] != name:
                        print("trigger")
                        cache[config['github_repo']] = name
                        # Post Discord embed about the latest release
                        request = requests.post(config['discord_webhook_url'], json={
                            "content": None,
                            "embeds": [
                                {
                                    "title": f"New release: {name}",
                                    "url": release_data["html_url"],
                                    "color": int(config['discord_color'], 16),
                                    "timestamp": published_date
                                }
                            ],
                            "username": config['discord_webhook_username'],
                            "avatar_url": config['discord_webhook_avatar']
                        })

                        if request.status_code != 204:
                            print(f"ERROR CODE {request.status_code}: {request.json()}")
                        else:
                            print(f"Latest release: {name}")
                            print(f"Tag name: {tag_name}")
                            print(f"Published date: {published_date}")
                            with open("cache.json", "w") as output_cache:
                                output_cache.write(json.dumps(cache))
                else:
                    # If the request was not successful, print an error message
                    print(f"Error fetching latest release: {response.status_code}")
            else:
                # Make a request to the GitHub API to fetch the tags of the repository
                url = f"https://github.com/{config['github_repo']}/tags.atom"
                feed = feedparser.parse(url)

                # Extract the name, tag name, and published date of the release
                name = feed.entries[0].title
                published_date = feed.entries[0].updated
                link = feed.entries[0].links[0].href

                # Check cache
                with open("cache.json", "r") as cache:
                    cache = json.load(cache)

                if config['github_repo'] not in cache:
                    cache[config['github_repo']] = "n/a"
                if cache[config['github_repo']] != name:
                    print("trigger")
                    cache[config['github_repo']] = name
                    # Post Discord embed about the latest release
                    request = requests.post(config['discord_webhook_url'], json={
                        "content": None,
                        "embeds": [
                            {
                                "title": f"New release: {name}",
                                "url": link,
                                "color": int(config['discord_color'], 16),
                                "timestamp": published_date
                            }
                        ],
                        "username": config['discord_webhook_username'],
                        "avatar_url": config['discord_webhook_avatar']
                    })
                    print(request.status_code)
                    if request.status_code != 201:
                        print(request.status_code)


                    print(f"Latest release: {name}")
                    print(f"Published date: {published_date}")
                    with open("cache.json", "w") as output_cache:
                        output_cache.write(json.dumps(cache))
    time.sleep(10*60) # 10 minutes
