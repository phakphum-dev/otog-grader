from constants.colors import colors


def bigPrint(header:str, text, color):
    print(f"[ {color}{header.upper()}{colors.RESET} ] {text}")


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
