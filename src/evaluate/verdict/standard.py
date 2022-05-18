from DTO.testcaseData import TestcaseData
from constants.Enums import VerdictStatus


def getVerdict(testCaseDto: TestcaseData):
    try:
        with open(testCaseDto.userPath) as f1, open(testCaseDto.solPath) as f2:
            while True:
                f1_line = f1.readline()
                f2_line = f2.readline()
                if f1_line == "" and f2_line == "":
                    return (VerdictStatus.accept, 1.0)
                if f1_line.rstrip() != f2_line.rstrip():
                    return (VerdictStatus.reject, 0.0)
    except:
        return (VerdictStatus.reject, 0.0)
