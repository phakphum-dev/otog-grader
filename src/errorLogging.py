import os
import requests
import json

from DTO.result import ResultDTO
from DTO.submission import SubmissionDTO
from handle import *
from constants.osDotEnv import osEnv
from message import *

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


def writeInternalErrorLog(submission: SubmissionDTO, result : ResultDTO):
    
    msg = genLogMDMessage(submission, result)

    #? check is ./testSpace/logs exist or not
    if not os.path.exists("./Logging/internalError"): os.mkdir("./Logging/internalError")

    with open(f"./Logging/internalError/{submission.id}.md", "w") as f:
        f.write(msg)

    #? send to discord
    if strToBool(osEnv.DISCORD_SEND_MESSAGE_WHEN_ERROR):
        payload = getDiscordUserSubPayload(submission, result)
        discordSend(payload)

def writeSubtaskErrorLog(submission: SubmissionDTO, errMsg : str):
    #? send to discord to notify problem author
    if strToBool(osEnv.DISCORD_SEND_MESSAGE_WHEN_ERROR):
        payload = getDiscordSubtaskPayload(submission, errMsg)
        discordSend(payload)

def getDiscordUserSubPayload(submission: SubmissionDTO, result : ResultDTO):
    fileStructureStr = f"{submission.problemId}/"
    filesStr = []
    for path, subdirs, files in os.walk(f"./source/{submission.problemId}"):
        for name in files:
            filesStr.append(os.path.join(path, name).removeprefix(f"./source/{submission.problemId}/"))
    filesStr = sorted(filesStr)
    fileStructureStr += "\n\t" + "\n\t".join(filesStr)

    msg = f""":skull::skull::skull: **ระบบของ SUB {submission.id} แตก!!!**:skull::skull::skull:

ผลตรวจ : `{result.result}`
ภาษา : `{submission.language}`

**Code**
```{submission.language}
{submission.sourceCode}
```

:warning:ที่ระบบด่ากลับมา
```
{result.errmsg}
```

:file_folder:Structure ในข้อที่ {submission.problemId}
```
{fileStructureStr}
```
"""

    payload = {
        "content": msg,
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "Submission",
                        "style": 5,
                        "url": f"{osEnv.OTOG_HOST}/submission/{submission.id}"
                    },
                    {
                        "type": 2,
                        "label": "User",
                        "style": 5,
                        "url": f"{osEnv.OTOG_HOST}/profile/{submission.userId}"
                    },
                    {
                        "type": 2,
                        "label": "Problem Doc",
                        "style": 5,
                        "url": f"{osEnv.OTOG_API}/problem/doc/{submission.problemId}"
                    }
                ]
            }
        ]
    }
    return payload


def getDiscordSubtaskPayload(submission: SubmissionDTO, errMsg : str):
    subtaskStr = "ไม่มีง่ะ"
    if os.path.exists(f"./source/{submission.problemId}/subtask.json"):
        with open(f"./source/{submission.problemId}/subtask.json", "r") as f:
            subtaskStr = f.read().strip()
    
    if len(subtaskStr) > 1000:
        subtaskStr = subtaskStr[:1000] + "..."
    elif len(subtaskStr) == 0:
        subtaskStr = "ไม่มีง่ะ"

    msg = f""":warning: Subtask ของ Problem {submission.problemId} แตก!!! :warning:

ข้อมูลจำนวนเทสเคสจาก Otog : `{submission.testcase}` (อาจไม่ได้ใช้ ถ้าใช้ subtask.json)

ข้อมูลจาก subtask.json
```json
{subtaskStr}
```

สาเหตุที่ระบบด่ากลับมา
```
{errMsg}
```
"""

    payload = {
        "content": msg,
        "components": [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "label": "Problem Doc",
                        "style": 5,
                        "url": f"{osEnv.OTOG_API}/problem/doc/{submission.problemId}"
                    },
                    {
                        "type": 2,
                        "label": "Subtask Wiki",
                        "style": 5,
                        "url": "https://github.com/phakphum-dev/otog-doc/wiki/%F0%9F%94%97-%E0%B8%84%E0%B8%B9%E0%B9%88%E0%B8%A1%E0%B8%B7%E0%B8%AD%E0%B8%AA%E0%B8%B3%E0%B8%AB%E0%B8%A3%E0%B8%B1%E0%B8%9A%E0%B8%81%E0%B8%B2%E0%B8%A3%E0%B9%80%E0%B8%9E%E0%B8%B4%E0%B9%88%E0%B8%A1-%E0%B9%81%E0%B8%81%E0%B9%89%E0%B9%84%E0%B8%82-%E0%B8%81%E0%B8%A5%E0%B8%B8%E0%B9%88%E0%B8%A1%E0%B8%97%E0%B8%94%E0%B8%AA%E0%B8%AD%E0%B8%9A-%E0%B9%81%E0%B8%9A%E0%B8%9A%E0%B9%83%E0%B8%AB%E0%B8%A1%E0%B9%88"
                    }
                ]
            }
        ]
    }
    return payload

def discordSend(payload):
    token = osEnv.DISCORD_BOT_TOKEN
    channel = osEnv.DISCORD_CHANNEL_ID

    headers = {
        "Authorization": f"Bot {token}",
        "Content-Type": "application/json"
    }
    url = f"https://discord.com/api/channels/{channel}/messages"

    # Send the API request to send the message
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code != 200:
        printFail("DISCORD", f"Fail to send message to discord\nresponse code : {response.status_code}\n{response.text}")
