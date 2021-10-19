import sys
import requests
import json
import re

# TODO: add more options like place of API-key, show relevant/time ordered comments, show only to-level comments, max number of comments etc...
# TODO: add a simple mode: no need for a regex. Like grep default. But also make it possible to use a regex with an cli-option
# TODO: make option to also show replies to comments


baseRESTFULurl = "https://www.googleapis.com/youtube/v3"


if len(sys.argv) == 2 and sys.argv[1].lower() == "help":
    print(sys.argv[0] + " <video-id> <regex>")
    exit(0)

if len(sys.argv) != 3:
    print("ERROR: Wrong number of arguments. Try \"" +
          sys.argv[0] + "help\" for a list of valid parameters")
    exit(1)

with open("./config.json") as f:
    config = json.load(f)

nextPageToken = None

while True:

    if nextPageToken:
        apiResult = requests.get(baseRESTFULurl +
                                 "/commentThreads?part=snippet%2Creplies&pageToken=" + nextPageToken + "&maxResults=100&videoId=" + sys.argv[1] + "&key=" + config["api_key"])
    else:
        apiResult = requests.get(baseRESTFULurl +
                                 "/commentThreads?part=snippet%2Creplies&maxResults=100&videoId=" + sys.argv[1] + "&key=" + config["api_key"])

    apiResultJSON = json.loads(apiResult.text)

    for commentObj in apiResultJSON["items"]:
        comment = commentObj["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        if re.match(sys.argv[2], comment):
            print(comment)

        try:
            replies = commentObj["replies"]["comments"]
            for reply in replies:
                if re.match(sys.argv[2], reply["snippet"]["textDisplay"]):
                    print(reply["snippet"]["textDisplay"])
        except KeyError:
            pass

    try:
        nextPageToken = apiResultJSON["nextPageToken"]
    except KeyError:
        break
