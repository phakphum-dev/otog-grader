from dataclasses import dataclass
from typing import List
from enum import Enum

class SubtaskOption(Enum):
    sum = "sum" # default

    max = "max"
    min = "min"


@dataclass
class SubtaskDTO:
    number: int
    cases: List[int]
    score: float
    group: bool
    require: List[int]
    option: SubtaskOption = SubtaskOption.sum


@dataclass
class ProblemTaskDTO:
    maxCase: int
    orderIndSubtask: List[int]
    subtasks: List[SubtaskDTO]


if __name__ == "__main__":
    bruh = SubtaskDTO([1, 2, 3], 13.0, False, [])
