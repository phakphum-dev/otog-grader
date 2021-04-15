from dataclasses import dataclass


@dataclass
class submissionDTO:
    def __init__(self, data):
        self.id = data[0]
        self.userId = data[1]
        self.problemId = data[2]
        self.contestId = data[8]
        self.sourceCode = data[9]
        self.language = data[10]
        self.mxScore = data[16]
        self.timeLimit = data[17]
        self.memoryLimit = data[18]
        self.testcase = data[21]
