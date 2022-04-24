from dataclasses import dataclass


@dataclass
class SubmissionDTO:
    id: int
    userId: int
    problemId: int
    contestId: int
    sourceCode: str
    language: str
    maxScore: int
    timeLimit: int
    memoryLimit: int
    testcase: str
    mode: str
