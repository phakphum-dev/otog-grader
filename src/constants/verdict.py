from constants.Enums import VerdictStatus
#from Enums import VerdictStatus


def verdictColorPat(status) -> str:
    if status == VerdictStatus.accept:
        return "\033[92m"  # ? Green
    elif status == VerdictStatus.reject:
        return "\033[91m"  # ? Red
    elif status == VerdictStatus.partial:
        return "\033[96m"  # ? blue
    elif status == VerdictStatus.runtimeErr:
        return "\033[95m"  # ? Magenta
    elif status == VerdictStatus.timeExceed:
        return "\033[33m"  # ? Orange
    elif status == VerdictStatus.skip:
        return "\033[90m"  # ? Grey
    elif status == VerdictStatus.err:
        return "\033[41m"  # ? Red with background
    else:
        return "\x1b[0m"  # ? Just Reset


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


def verdictCodeforces(status: VerdictStatus) -> str:
    if status == VerdictStatus.accept:
        return "Accepted"
    elif status == VerdictStatus.partial:
        return "Partial correct on pretest %d"
    elif status == VerdictStatus.reject:
        return "Wrong answer on pretest %d"
    elif status == VerdictStatus.timeExceed:
        return "Time limit exceeded on pretest %d"
    elif status == VerdictStatus.runtimeErr:
        return "Runtime error on pretest %d"
    elif status == VerdictStatus.skip:
        return "Skipping on pretest %d"  # ? not use
    else:
        return "Judge error on pretest %d"


def verdictColorFormat(status: VerdictStatus, content: str) -> str:
    return f"{verdictColorPat(status)}{content}{verdictColorPat('RESET')}"


def verdictsColorSymbol(status: VerdictStatus) -> str:
    return verdictColorFormat(status, verdictSymbol(status))


def verdictsColorCodeforces(status: VerdictStatus) -> str:
    return verdictColorFormat(status, verdictCodeforces(status))


if __name__ == "__main__":
    print(verdictsColorSymbol(VerdictStatus.accept),
          verdictsColorSymbol(VerdictStatus.partial),
          verdictsColorSymbol(VerdictStatus.reject),
          verdictsColorSymbol(VerdictStatus.runtimeErr),
          verdictsColorSymbol(VerdictStatus.timeExceed),
          verdictsColorSymbol(VerdictStatus.skip),
          verdictsColorSymbol(VerdictStatus.err)
          )
