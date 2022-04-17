from constants.osDotEnv import *

dbConfig = {
    "host": osEnv.POSTGRES_HOST,
    "port": osEnv.POSTGRES_PORT,
    "user": osEnv.POSTGRES_USER,
    "password": osEnv.POSTGRES_PASSWD,
    "dbname": osEnv.POSTGRES_DATABASE,
}