from enum import Enum

class JudgeType( Enum ):
    ogogi = "ogogi"
    cppCheck = "check.cpp"
    standard = "standard"


if __name__ == "__main__":
    print(JudgeType.ogogi.value)