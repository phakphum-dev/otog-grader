import configparser

config = configparser.ConfigParser()
try:
    config.read("./config.ini")
except:
    print("config.ini not found...")
    exit(1)


dbConfig = {
    "host": config["postgres"]["host"],
    "port": config["postgres"]["port"],
    "user": config["postgres"]["user"],
    "password": config["postgres"]["passwd"],
    "dbname": config["postgres"]["database"],
}
