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

if __name__ == "__main__":
    print(get("grader", "max_error_line"))
