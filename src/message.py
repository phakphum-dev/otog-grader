from constants.colors import colors


def bigPrint(header: str, text, color, colorAll = False):
    lines = text.split("\n")
    for i, eachLine in enumerate(lines):
        if i == 0:  # ? print name only first line
            print(f"[ {color}{header.upper()}{colors.RESET} ]", end=" ")
        else:
            print(f"{' '*(len(header) + 4)}", end=" ")

        if colorAll:
            print(f"{color}{eachLine.strip()}{colors.RESET}")
        else:
            print(f"{eachLine.strip()}")


def printBlod(header, text):
    bigPrint(header, text, colors.BOLD)


def printEndC(header, text):
    bigPrint(header, text, colors.ENDC)


def printFail(header, text):
    bigPrint(header, text, colors.FAIL)


def printHeader(header, text):
    bigPrint(header, text, colors.HEADER)


def printOKBlue(header, text):
    bigPrint(header, text, colors.OKBLUE)


def printOKCyan(header, text):
    bigPrint(header, text, colors.OKCYAN)


def printOKGreen(header, text):
    bigPrint(header, text, colors.OKGREEN)


def printUnderline(header, text):
    bigPrint(header, text, colors.UNDERLINE)


def printWarning(header, text):
    bigPrint(header, text, colors.WARNING)
