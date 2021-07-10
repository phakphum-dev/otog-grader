import configparser

config = configparser.ConfigParser()
try:
    config.read("./config.ini")
except:
    print("config.ini not found...")
    exit(1)


dbConfig = {
    "host": config["mysql"]["host"],
    "port": config["mysql"]["port"],
    "user": config["mysql"]["user"],
    "passwd": config["mysql"]["passwd"],
    "database": config["mysql"]["database"],
}
