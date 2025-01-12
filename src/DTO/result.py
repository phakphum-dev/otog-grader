from dataclasses import dataclass
from typing import List
from DTO.groupResult import GroupResult


@dataclass
class ResultDTO:
    id: int
    result: str
    score: int
    sumTime: int
    memUse: int
    errmsg: str
    # fullResult: List[GroupResult]
