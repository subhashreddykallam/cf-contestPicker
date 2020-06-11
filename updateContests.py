import requests
from bs4 import BeautifulSoup
import json

def getContestData():
    url = "https://codeforces.com/api/contest.list"
    url_dump = requests.get(url)
    data = url_dump.json()
    return data
    for contest in data["result"]:
        if contest["phase"] == "FINISHED":
            max_id = contest["id"]
            break
    return max_id

def getExistingData():
    allContests = {}
    try:
        with open("allContests.json", "r") as f:
            allContests = json.load(f)
    except:
        with open("allContests.json", "w") as f:
            json.dump(allContests, f)
        with open("allContests.json", "r") as f:
            allContests = json.load(f)
    return allContests

def update(allContests, data):
    for contest in data["result"]:
        if contest["phase"]!="FINISHED":
            continue
        contest_id = contest["id"]
        if str(contest_id) in allContests:
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
    return allContests

def writeToFile(data):
    with open("allContests.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    contestData = getContestData()
    existingData = getExistingData()
    updatedData = update(existingData, contestData)
    writeToFile(updatedData)