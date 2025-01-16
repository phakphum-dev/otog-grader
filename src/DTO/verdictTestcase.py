from dataclasses import dataclass
from constants.Enums import VerdictStatus


@dataclass
class VerdictTestcase:
    status: VerdictStatus
    percent: float
    # ? from 0 to 1 (between is accepted e.g. 0.69)
    timeUse: float
    memUse: int

    def to_dict(self):
        return {
            "status": self.status.value,
            "percent": self.percent,
            "timeUse": self.timeUse,
            "memUse": self.memUse
        }
