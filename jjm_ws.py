from bs4 import BeautifulSoup
from bs4.element import Tag
import requests

from typing import List, Tuple
from sys import argv, exit

EVENT_SUCCESS_INDEX = 6
EVENT_FAILURE_INDEX = 7
EVENT_DURATION_INDEX = 8

E_GREEN_CHECK = "\U00002705"
E_RED_CROSS = "\U0000274c"
E_GREY_WORKING = "\U0001F916"
E_SUCCESS = "\U0001F60E"
E_FAIL = "\U0001F635"
E_DURATION = "\U000023F1"
E_JOB = "\U0001F4C1"


def getProcessName(soup:BeautifulSoup) -> str:
    return soup.h1.text.strip()


def getJobName(rowTag:Tag) -> str:
    return rowTag["id"].replace("job_", "")


def getJobStatus(rowTag:Tag) -> str:
    return rowTag.find("img")["alt"]


def getJobDuration(rowTag: Tag, eventIndex:int = EVENT_SUCCESS_INDEX) -> str:
    eventText = rowTag.findAll("td")[eventIndex].text
    if "-" in eventText:
        return eventText.split("-")[0].strip()
    return eventText.strip()


def processJenkinsRow(row:Tag) -> Tuple[str, str, str, str, str]:
    jobName = getJobName(row)
    jobStatus = getJobStatus(row)
    success = getJobDuration(row, EVENT_SUCCESS_INDEX)
    failure = getJobDuration(row, EVENT_FAILURE_INDEX)
    duration = getJobDuration(row, EVENT_DURATION_INDEX)
    return (jobName, jobStatus, success, failure, duration)


def prettyfyProcessName(processName:str) -> str:
    return E_JOB + " \033[1m" + processName + "\033[0m"


def prettifyRow(info:Tuple[str, str, str, str, str]) -> str:
    sessionName:str = info[0].ljust(50)
    statusEmoji:str = E_RED_CROSS
    if info[1] == "Success":
        statusEmoji = E_GREEN_CHECK
    elif info[1] == "In progress":
        statusEmoji = E_GREY_WORKING
    return "  {} \033[1m{} \033[0m {}{} {}{} {} {} ".format(statusEmoji, sessionName, E_SUCCESS, info[2], E_FAIL, info[3], E_DURATION, info[4])
    
def safeContent(url:str) -> Tuple[bool, str]:
    try:
        return (False, requests.get(url).text)
    except:
        return (True, "")


def processURL(url:str) -> None:
    content: str = requests.get(url).text
    soup: BeautifulSoup = BeautifulSoup(content, "html.parser")
    processName:str = getProcessName(soup)
    table:Tag = soup.find("table", id="projectstatus")

    # Filter only the data rows, and ignore the header and inactive rows
    rows:List[Tag] = [r for r in table.findAll("tr") if "id" in r.attrs]
    rows = [r for r in rows if "job-status-nobuilt" not in r["class"]]

    print("{}".format(prettyfyProcessName(processName)))

    report:List[Tuple[str, str, str, str, str]] = [prettifyRow(processJenkinsRow(row)) for row in rows] 
    for info in report:
        print(info)


def processURLFile(filePath:str) -> None:
    try:
        with open(filePath, "r") as urlsFile:
            urls:List[str] = urlsFile.readlines()
            for url in urls:
                processURL(url.replace("\n", ""))
    except:
        print("File {} does not exists".format(filePath))
        exit(1)

def printHelp() -> None:
    helpString = """Jenkins job monitor
    USAGE: jjm [[--input-url | -u URL] | [--input-urls-file | -i FILE_PATH]] 
    """
    print(helpString)

if __name__ == "__main__":
    if len(argv) != 3:
        printHelp()
        exit(1)

    if argv[1] in ["--input-url", "-u"]:
        processURL(argv[2])
    elif argv[1] in ["--input-urls-file", "-i"]:
        processURLFile(argv[2])

#url: str = "https://big-data-jenkins-prod.bigdata.expedia.com/job/ede/job/ede-mops-app-google-searchanalytics-prod/"

