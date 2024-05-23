import datetime
import os
import requests
import json

from DTO.result import ResultDTO
from DTO.submission import SubmissionDTO
from handle import *
from constants.osDotEnv import osEnv
from message import *
from constants.verdict import verdictCodeforces, verdictSymbol


isDiscordErrorSend = strToBool(osEnv.DISCORD_SEND_MESSAGE_WHEN_ERROR)
token = osEnv.DISCORD_BOT_TOKEN
channel = osEnv.DISCORD_CHANNEL_ID

def genLogMDMessage(submission: SubmissionDTO, result : ResultDTO, tabLevel : int = 1):
    s = "#" * (tabLevel - 1)
    msg = f"""{s}# Submission : {submission.id}

**user ID** : {submission.userId}

**problem ID** : {submission.problemId}

<details>
  <summary>Problem Data</summary>
  
  Number of testcase : {submission.testcase}
  
  Time limit : {submission.timeLimit}

  Memory limit : {submission.memoryLimit}

</details>

{s}## Result

| Result   | {result.result}  |
|----------|------------------|
| Score    | {result.score}   |
| Time use | {result.sumTime} |
| Mem use  | {result.memUse}  |
| Comment  | {result.errmsg}  |

{s}## code

```{submission.language}
{submission.sourceCode}
```
"""

    return msg

def discordSendMsg(payload, channel = channel):

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/channels/{channel}/messages"

    # Send the API request to send the message
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code < 200 or response.status_code >= 300:
        printFail("DISCORD", f"Fail to send message to discord\nresponse code : {response.status_code}\n{response.text}")
    else:
        return response.json()

def discordCreateThread(idMsg, name):

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/channels/{channel}/messages/{idMsg}/threads"

    # Send the API request to send the message
    response = requests.post(url, headers=headers, data=json.dumps({"name": name,}))

    # Check if the request was successful
    if response.status_code < 200 or response.status_code >= 300:
        printFail("DISCORD", f"Fail to create thread\nresponse code : {response.status_code}\n{response.text}")
    else:
        return response.json()

def getSubLinkContent(submission: SubmissionDTO):
    return  [
            {
            "type": 1,
            "components": [
                {
                "type": 2,
                "style": 5,
                "label": "Submission",
                "url": f"{osEnv.OTOG_HOST}/submission/{submission.id}",
                "emoji": {
                    "name": "🖥",
                    "animated": False
                },
                },
                {
                "type": 2,
                "style": 5,
                "label": "User",
                "url": f"{osEnv.OTOG_HOST}/profile/{submission.userId}",
                "emoji": {
                    "name": "👤",
                    "animated": False
                },
                },
                {
                "type": 2,
                "style": 5,
                "label": "Problem Doc",
                "url": f"{osEnv.OTOG_API}/problem/doc/{submission.problemId}",
                "emoji": {
                    "name": "📄",
                    "animated": False
                },
                },
            ]
            }
        ]

def getProblemFileStructure(submission: SubmissionDTO):
    fileStructureStr = f"{submission.problemId}/"
    filesStr = []
    for path, subdirs, files in os.walk(f"./source/{submission.problemId}"):
        for name in files:
            filesStr.append(os.path.join(path, name).removeprefix(f"./source/{submission.problemId}/"))
    filesStr = sorted(filesStr)
    fileStructureStr += "\n\t" + "\n\t".join(filesStr)
    return fileStructureStr

def getDiscordUserSubPayloads(submission: SubmissionDTO, result : ResultDTO, errorCode = "error code"):
    fileStructureStr = getProblemFileStructure(submission)

    mainPayload = {
        "embeds": [
            {
            "title": f":skull:ระบบของ Submission {submission.id} แตก!!!",
            "description": f"ข้อที่ : `{submission.problemId}`\nผลตรวจ : `{result.result}`\nภาษา : `{submission.language}`\n:warning: ที่ระบบด่ากลับมา\n```\n{result.errmsg}\n```",
            "color": 15409955,
            "fields": [],
            "timestamp": getNowTimeStamp(),
            "footer": {
                "text": errorCode
            },
            }
        ],
        "components": getSubLinkContent(submission)
    }

    msg = f"""
ภาษา : `{submission.language}`

**Code**
```{submission.language}
{submission.sourceCode}
```

:file_folder:Structure ในข้อที่ {submission.problemId}
```
{fileStructureStr}
```
"""

    detailsPayload = {
        "content": msg,
        "components": getSubLinkContent(submission)
    }


    return [mainPayload, detailsPayload]


def getDiscordTestcaseErrorPayloads(submission: SubmissionDTO, errMsg : str, isSubtaskError = False):
    subtaskStr = "ไม่มีง่ะ"
    if os.path.exists(f"./source/{submission.problemId}/subtask.json"):
        with open(f"./source/{submission.problemId}/subtask.json", "r") as f:
            subtaskStr = f.read().strip()
    
    if len(subtaskStr) > 1000:
        subtaskStr = subtaskStr[:1000] + "..."
    elif len(subtaskStr) == 0:
        subtaskStr = "ไม่มีง่ะ"

    components = [
                    {
                        "type": 2,
                        "label": "Problem Doc",
                        "style": 5,
                        "url": f"{osEnv.OTOG_API}/problem/doc/{submission.problemId}",
                        "emoji": {
                            "name": "📄",
                            "animated": False
                        },
                    },
                ]
    if isSubtaskError:
        components.append(
            {
                "type": 2,
                "label": "Subtask Wiki",
                "style": 5,
                "url": "https://github.com/phakphum-dev/otog-doc/wiki/%F0%9F%94%97-%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%9E%E0%B8%B4%E0%B9%88%E0%B8%A1-%E0%B9%81%E0%B8%81%E0%B9%89%E0%B9%84%E0%B8%82-%E0%B8%81%E0%B8%A5%E0%B8%B8%E0%B9%88%E0%B8%A1%E0%B8%97%E0%B8%94%E0%B8%AA%E0%B8%AD%E0%B8%9A-%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88",
                "emoji": {
                    "name": "❓",
                    "animated": False
                },
            }
        )
    
    subtaskTitle = " subtask ของ" if isSubtaskError else ""
    mainPayload = {
        "embeds": [
            {
            "title": f":skull:{subtaskTitle} Problem {submission.problemId} แตก!!! :skull:",
            "description": f"สาเหตุที่ระบบด่ากลับมา\n```\n{errMsg}\n```",
            "color": 15409955,
            "fields": [],
            "timestamp": getNowTimeStamp(),
            "footer": {
                "text": "SUBTASK ERROR" if isSubtaskError else "TESTCASE ERROR"
            },
            }
        ],
        "components": [{
            "type": 1,
            "components": components
        }]
    }

    if isSubtaskError:

        msg = f"""ข้อมูลจำนวนเทสเคสจาก Otog : `{submission.testcase}` (อาจไม่ได้ใช้ ถ้าใช้ subtask.json)

ข้อมูลจาก subtask.json
```json
{subtaskStr}
```"""
    else:
        msg = f""":file_folder:Structure ในข้อที่ `{submission.problemId}` (ถ้าอยากรู้)
```
{getProblemFileStructure(submission)}
```
"""

    detailsPayload = {
        "content": msg,
        "components": [{
            "type": 1,
            "components": components
        }]
    }


    return [mainPayload, detailsPayload]


def writeInternalErrorLog(submission: SubmissionDTO, result : ResultDTO, errorCode):
    
    msg = genLogMDMessage(submission, result)

    #? check is ./testSpace/logs exist or not
    if not os.path.exists("./Logging/internalError"): os.mkdir("./Logging/internalError")

    with open(f"./Logging/internalError/{submission.id}.md", "w") as f:
        f.write(msg)

    #? send to discord
    if isDiscordErrorSend:
        mainPayload, detailPayload = getDiscordUserSubPayloads(submission, result, errorCode)
        cId = discordSendMsg(mainPayload)["id"]
        discordCreateThread(cId, f"Grader ระเบิด!! ({submission.id})")
        discordSendMsg(detailPayload, cId)

wSubIdPrev = -1
def writeInternalWarningLog(submission: SubmissionDTO, errorMsg : str, verdict : VerdictStatus, errorCode):
    global wSubIdPrev
    if wSubIdPrev == submission.id:
        return
    wSubIdPrev = submission.id
    treatVerdict = f"{verdictSymbol(verdict)}"
    #? send to discord
    if isDiscordErrorSend:
        payload = {
            "embeds": [
            {
            "title": f":warning: Warning ใน Submission {submission.id}",
            "description": f"ข้อที่ : `{submission.problemId}`\nภาษา : `{submission.language}`\n:warning: ที่ระบบด่ากลับมา\n```{errorMsg}```\n:arrows_counterclockwise: มีผลตรวจเป็น : `{treatVerdict}`",
            "color": 15451427,
            "fields": [],
            "timestamp": getNowTimeStamp(),
            "footer": {
                "text": errorCode
            },
            }
        ],
            "components": getSubLinkContent(submission)
        }

        discordSendMsg(payload)

def writeSubtaskErrorLog(submission: SubmissionDTO, errMsg : str):
    #? send to discord to notify problem author
    if isDiscordErrorSend:
        mainPayload, detailPayload = getDiscordTestcaseErrorPayloads(submission, errMsg, True)
        cId = discordSendMsg(mainPayload)["id"]
        discordCreateThread(cId, f"Subtask ระเบิด!! ({submission.id})")
        discordSendMsg(detailPayload, cId)

def writeTestcaseErrorLog(submission: SubmissionDTO, errMsg : str):
    #? send to discord to notify problem author
    if isDiscordErrorSend:
        mainPayload, detailPayload = getDiscordTestcaseErrorPayloads(submission, errMsg, False)
        cId = discordSendMsg(mainPayload)["id"]
        discordCreateThread(cId, f"โจทย์ ระเบิด!! ({submission.id})")
        discordSendMsg(detailPayload, cId)