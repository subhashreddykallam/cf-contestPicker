import requests
from bs4 import BeautifulSoup
import json

url = "https://codeforces.com/api/contest.list"
url_dump = requests.get(url)
data = url_dump.json()

for contest in data["result"]:
    if contest["phase"] == "FINISHED":
        max_id = contest["id"]
        break

f = open("allContests.json")
allContests = json.load(f)
f.close()

for contest_id in range(1, max_id+1):
    if contest_id in allContests:
        continue
    print(contest_id)
    page = requests.get("https://codeforces.com/contest/"+str(contest_id))
    page = BeautifulSoup(page.content, "html.parser")
    flag = False
    problems = []
    for i in page.find_all("option"):
        text = i.get_text()
        if text == "Choose problem":
            if flag:
                break
            else:
                flag = True
        else:
            problems.append(text.split()[0])
    allContests[contest_id] = problems
    break

with open("allContests.json", "w") as f:
    json.dump(allContests, f)
