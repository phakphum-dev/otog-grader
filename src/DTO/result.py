from dataclasses import dataclass


@dataclass
class ResultDTO:
    id: int
    result: str
    score: int
    sumTime: int
    memUse: int
    errmsg: str
