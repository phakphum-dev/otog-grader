from dataclasses import dataclass


@dataclass
class submissionDTO:
    def __init__(self, submissionId, userId, problemId,
    contestId, sourceCode, language, maxScore, timeLimit,
    memoryLimit, testcase, mode):
        self.id = submissionId
        self.userId = userId
        self.problemId = problemId
        self.contestId = contestId
        self.sourceCode = sourceCode
        self.language = language
        self.mxScore = maxScore
        self.timeLimit = timeLimit
        self.memoryLimit = memoryLimit
        self.testcase = testcase
        self.mode = mode
