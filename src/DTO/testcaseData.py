from dataclasses import dataclass


@dataclass
class TestcaseData:
    userPath: str  # ? User output
    solPath: str  # ? sol

    testCase: int  # ? #testcase
    srcPath: str  # ? source code path
