import os

class osEnv:
    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWD = os.environ['POSTGRES_PASSWD']
    POSTGRES_DATABASE = os.environ['POSTGRES_DATABASE']

    GRADER_MAX_ERROR_LINE = os.environ['GRADER_MAX_ERROR_LINE'] or "300"
    GRADER_TIME_FACTOR = os.environ['GRADER_TIME_FACTOR'] or "1"
    GRADER_USE_ISOLATE = os.environ['GRADER_USE_ISOLATE'] or "True"

if __name__ == "__main__":
    print(osEnv.POSTGRES_HOST)
    print(osEnv.POSTGRES_DATABASE)
    print(osEnv.GRADER_MAX_ERROR_LINE)
    print(osEnv.GRADER_TIME_FACTOR)
    print(osEnv.GRADER_USE_ISOLATE)