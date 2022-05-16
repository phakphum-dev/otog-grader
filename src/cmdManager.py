import yaml
import os

import constants.command as defCmd
import message as mes


useConfigFrom = "constants"
commandData = None

if os.path.exists(f"./command.yaml"):
    try:
        with open(f"./command.yaml", "r") as f:
            command = f.read()
        commandData = yaml.load(command, Loader=yaml.FullLoader)
    except:
        mes.printFail("command", "can't read command.yaml")
else:
    mes.printUnderline("command", "command.yaml not found... use default")

if type(commandData) == type(dict()):
    if "version" not in commandData or commandData["version"] != defCmd.version:
        mes.printWarning(
            "command", "mismatch version... please update your command.yaml")
        mes.printWarning("command", "use default")
    else:
        mes.printOKCyan("command", "command.yaml founded... use command.yaml")
        useConfigFrom = "yml"


def get(lang: str, content: str):
    if useConfigFrom == "yml":
        return commandData[lang][content]
    else:
        return defCmd.langarr[lang][content]
