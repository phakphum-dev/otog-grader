from dotenv import load_dotenv, dotenv_values 
import os

load_dotenv(".env")

class osEnv:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWD = os.getenv('POSTGRES_PASSWD')
    POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

    # LOAD BALANCE
    LOAD_BALANCE_N_GRADER = os.getenv('LOAD_BALANCE_N_GRADER') or "1"
    LOAD_BALANCE_THIS_GRADER = os.getenv('LOAD_BALANCE_THIS_GRADER') or "1"

    GRADER_MAX_ERROR_LINE = os.getenv('GRADER_MAX_ERROR_LINE') or "300"
    GRADER_TIME_FACTOR = os.getenv('GRADER_TIME_FACTOR') or "1"
    GRADER_ENABLE_OFFLINE_LOGGING = os.getenv('GRADER_ENABLE_OFFLINE_LOGGING') or "False"
    GRADER_FORCE_TO_MODE = os.getenv('GRADER_FORCE_TO_MODE') or "none"

    USE_ISOLATE = os.getenv('USE_ISOLATE') or "True"
    USE_CONTROL_GROUP = os.getenv('USE_CONTROL_GROUP') or "False"

    SYNC_HOST = os.getenv('SYNC_HOST')
    SYNC_PORT = os.getenv('SYNC_PORT')

    DISCORD_SEND_MESSAGE_WHEN_ERROR = os.getenv('DISCORD_SEND_MESSAGE_WHEN_ERROR') or "False"
    DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN') or ""
    DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID') or ""

    OTOG_HOST = os.getenv('OTOG_HOST')
    OTOG_API = os.getenv('OTOG_API')


if __name__ == "__main__":
    print(osEnv.POSTGRES_HOST)
    print(osEnv.POSTGRES_DATABASE)
    print(osEnv.GRADER_MAX_ERROR_LINE)
    print(osEnv.GRADER_TIME_FACTOR)
    print(osEnv.GRADER_USE_ISOLATE)
