from enum import Enum


class EvaluateMode(Enum):
    classic = "classic"
    codeforces = "codeforces"


class JudgeType(Enum):
    ogogi = "ogogi"
    cppCheck = "check.cpp"
    standard = "standard"

    thaco = "thaco"  # ? https://thaco.tech


class VerdictStatus(Enum):
    accept = "accept"
    partial = "partial"
    reject = "reject"

    timeExceed = "time limit exceed"
    runtimeErr = "runtime error"

    skip = "skip"

    err = "error"
