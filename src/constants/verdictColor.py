

class verdictColorPat:
    ACCEPT      = "\033[92m" #? Green
    WRONG       = "\033[91m" #? Red
    RUNTIME_ERR = "\033[95m" #? Magenta
    TIME_EXCEED = "\033[33m" #? Orange
    SKIP        = "\033[90m" #? Grey
    ERROR       = "\033[1m"  #? BOLD
    RESET       = "\x1b[0m"  #? Just Reset

verdictsColor = {
    "P" : verdictColorPat.ACCEPT      + "P" + verdictColorPat.RESET,
    "-" : verdictColorPat.WRONG       + "-" + verdictColorPat.RESET,
    "X" : verdictColorPat.RUNTIME_ERR + "X" + verdictColorPat.RESET,
    "T" : verdictColorPat.TIME_EXCEED + "T" + verdictColorPat.RESET,
    "S" : verdictColorPat.SKIP        + "S" + verdictColorPat.RESET,
    "!" : verdictColorPat.ERROR       + "!" + verdictColorPat.RESET,
}

if __name__ == "__main__":
    print(verdictsColor["P"],
    verdictsColor["T"],
    verdictsColor["-"],
    verdictsColor["X"],
    verdictsColor["S"],
    verdictsColor["!"])