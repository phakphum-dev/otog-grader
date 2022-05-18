import configparser

config = configparser.ConfigParser()
try:
    config.read("./config.ini")
except:
    print("config.ini not found...")
    exit(1)


def get(*args):
    entity = config

    for e in args:
        entity = entity[e]
    return entity


def getAsBool(*args) -> bool:
    entity = config

    for e in args:
        entity = entity[e]

    if entity.lower() == "false":
        return False
    return True


def getAs(type, *args):
    entity = config

    for e in args:
        entity = entity[e]

    return type(entity)


if __name__ == "__main__":
    print(get("grader", "max_error_line"))
    print(type(getAs(int, "grader", "max_error_line")),
          getAs(int, "grader", "max_error_line"))
    print(type(getAs(bool, "grader", "max_error_line")),
          getAs(bool, "grader", "max_error_line"))
