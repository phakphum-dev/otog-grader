import os


class osEnv:
    POSTGRES_HOST = os.environ['POSTGRES_HOST']
    POSTGRES_PORT = os.environ['POSTGRES_PORT']
    POSTGRES_USER = os.environ['POSTGRES_USER']
    POSTGRES_PASSWD = os.environ['POSTGRES_PASSWD']
    POSTGRES_DATABASE = os.environ['POSTGRES_DATABASE']

    # LOAD BALANCE
    LOAD_BALANCE_N_GRADER = os.environ['LOAD_BALANCE_N_GRADER'] or "1"
    LOAD_BALANCE_THIS_GRADER = os.environ['LOAD_BALANCE_THIS_GRADER'] or "1"

    GRADER_MAX_ERROR_LINE = os.environ['GRADER_MAX_ERROR_LINE'] or "300"
    GRADER_TIME_FACTOR = os.environ['GRADER_TIME_FACTOR'] or "1"
    GRADER_ENABLE_OFFLINE_LOGGING = os.environ['GRADER_ENABLE_OFFLINE_LOGGING'] or "False"
    GRADER_FORCE_TO_MODE = os.environ['GRADER_FORCE_TO_MODE'] or "none"

    USE_ISOLATE = os.environ['USE_ISOLATE'] or "True"
    USE_CONTROL_GROUP = os.environ['USE_CONTROL_GROUP'] or "False"

    SYNC_HOST = os.environ['SYNC_HOST']
    SYNC_PORT = os.environ['SYNC_PORT']

    DISCORD_SEND_MESSAGE_WHEN_ERROR = os.environ['DISCORD_SEND_MESSAGE_WHEN_ERROR'] or "False"
    DISCORD_BOT_TOKEN = os.environ['DISCORD_BOT_TOKEN'] or ""
    DISCORD_CHANNEL_ID = os.environ['DISCORD_CHANNEL_ID'] or ""


if __name__ == "__main__":
    print(osEnv.POSTGRES_HOST)
    print(osEnv.POSTGRES_DATABASE)
    print(osEnv.GRADER_MAX_ERROR_LINE)
    print(osEnv.GRADER_TIME_FACTOR)
    print(osEnv.GRADER_USE_ISOLATE)
