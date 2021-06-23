import configparser

configINI = configparser.ConfigParser()
try:
    configINI.read("./BigConfig.ini")
except:
    print("BigConfig.ini not found...")
    exit(1)



dbConfig = {
    "host": configINI["mySQL"]["host"],
    "port": configINI["mySQL"]["port"],
    "user": configINI["mySQL"]["user"],
    "passwd": configINI["mySQL"]["passwd"],
    "database": configINI["mySQL"]["database"],
}
