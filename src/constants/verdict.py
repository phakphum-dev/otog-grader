from constants.Enums import VerdictStatus
#from Enums import VerdictStatus


def verdictColorPat(status) -> str:
    if status == VerdictStatus.accept:
        return "\033[92m" #? Green
    elif status == VerdictStatus.reject:
        return "\033[91m" #? Red
    elif status == VerdictStatus.partial:
        return "\033[96m" #? blue
    elif status == VerdictStatus.runtimeErr:
        return "\033[95m" #? Magenta
    elif status == VerdictStatus.timeExceed:
        return "\033[33m" #? Orange
    elif status == VerdictStatus.skip:
        return "\033[90m" #? Grey
    elif status == VerdictStatus.err:
        return "\033[41m"  #? Red with background
    else:
        return "\x1b[0m"  #? Just Reset

def verdictSymbol(status: VerdictStatus) -> str:
    if status == VerdictStatus.accept:
        return "P"
    elif status == VerdictStatus.reject:
        return "-"
    elif status == VerdictStatus.partial:
        return "%"
    elif status == VerdictStatus.runtimeErr:
        return "X"
    elif status == VerdictStatus.timeExceed:
        return "T"
    elif status == VerdictStatus.skip:
        return "S"
    else:
        return "!"

def verdictsColorSymbol(status: VerdictStatus) -> str:
    return verdictColorPat(status) + verdictSymbol(status) + verdictColorPat("RESET")


if __name__ == "__main__":
    print(verdictsColorSymbol(VerdictStatus.accept),
    verdictsColorSymbol(VerdictStatus.partial),
    verdictsColorSymbol(VerdictStatus.reject),
    verdictsColorSymbol(VerdictStatus.runtimeErr),
    verdictsColorSymbol(VerdictStatus.timeExceed),
    verdictsColorSymbol(VerdictStatus.skip),
    verdictsColorSymbol(VerdictStatus.err)
    )