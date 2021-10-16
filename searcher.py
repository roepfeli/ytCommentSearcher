import sys
import requests
import json

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

comments = requests.get(baseRESTFULurl +
                        "/commentThreads?part=snippet%2Creplies&videoId=" + sys.argv[1] + "&key=" + config["api_key"])

# print(comments.text)

for comment in json.loads(comments.text)["items"]:
    print(comment["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
