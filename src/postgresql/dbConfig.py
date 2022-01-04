import config

dbConfig = {
    "host": config.get("postgres", "host"),
    "port": config.get("postgres", "port"),
    "user": config.get("postgres", "user"),
    "password": config.get("postgres", "passwd"),
    "dbname": config.get("postgres", "database"),
}
