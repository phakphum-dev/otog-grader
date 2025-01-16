from dataclasses import dataclass
from typing import List
from DTO.verdictTestcase import VerdictTestcase


@dataclass
class GroupResult:
    score: float
    fullScore: float
    verdicts: List[VerdictTestcase]

    def to_dict(self):
        return {
            "score": self.score,
            "fullScore": self.fullScore,
            "verdicts": [verdict.to_dict() for verdict in self.verdicts]
        }


@dataclass
class ResultDTO:
    id: int
    result: str
    score: int
    sumTime: int
    memUse: int
    errmsg: str
    fullResult: List[GroupResult]
