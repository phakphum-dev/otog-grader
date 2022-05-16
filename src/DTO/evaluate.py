
from DTO.submission import SubmissionDTO
from dataclasses import dataclass
from constants.Enums import EvaluateMode, JudgeType


@dataclass
class EvaluateData:
    submission: SubmissionDTO
    srcPath: str
    evaluateMode: EvaluateMode
    judgeType: JudgeType
