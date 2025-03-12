from dataclasses import dataclass
from typing import List
from enum import Enum

class ContestMode(Enum):
    ACM = "acm"
    CLASSIC = "classic"
    BEST_SUBMISSION = "bestSubmission"
    BEST_SUBTASK = "bestSubtask"


@dataclass
class ContestScoreHistoryDTO:
    submissionId: int
    score: int


@dataclass
class ContestScoreDTO:
    id: int
    score: int
    history: List[ContestScoreHistoryDTO]
