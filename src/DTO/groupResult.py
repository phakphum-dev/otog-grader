from dataclasses import dataclass
from typing import List
from DTO.verdictTestcase import VerdictTestcase


@dataclass
class GroupResult:
    score: float
    fullScore: float
    verdicts: List[VerdictTestcase]
