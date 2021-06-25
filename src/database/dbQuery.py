from constants.colors import bcolors
from .dbInit import DB
from datetime import datetime
import time
import socketio
import configparser

db = DB()
socketIO = socketio.Client()


def testDBConnection():
    try:
        db.connect()
    except Exception as e:
        print(f"[ {bcolors.FAIL}MYSQL{bcolors.RESET} ] Connection failed.")
        print(f"[ {bcolors.FAIL}MYSQL{bcolors.RESET} ] {e}")
        exit(1)
    print(
        f"{bcolors.OKGREEN}[ MYSQL ] Connect MYSQL success fully!.{bcolors.RESET}")
    DBDisconnect()


def DBConnect():
    try:
        db.connect()
    except:
        for i in range(5):
            try:
                print(
                    f"{bcolors.WARNING}[ MYSQL ] Connection failed, retrying in ({i+1}) secs...{bcolors.RESET}"
                )
                time.sleep(i + 1)
                db.connect()
                print(
                    f"{bcolors.OKGREEN}[ MYSQL ] Connect MYSQL success fully!.{bcolors.RESET}")
                return
            except:
                pass
        print(f"{bcolors.FAIL}[ MYSQL ] Connection Lost.{bcolors.RESET}")
        exit(1)


def DBDisconnect():
    db.disconnect()


def getsocketIO():
    return socketIO


def socketTestConnect():

    configINI = configparser.ConfigParser()
    try:
        configINI.read("./BigConfig.ini")
    except:
        print("BigConfig.ini not found...")
        exit(1)

    URL = configINI["socket"]["URL"]
    secret = configINI["socket"]["secret"]
    keySocket = configINI["socket"]["keySocket"]
    try:
        socketIO.connect(URL, headers={"key": keySocket}, auth={
                         "token": secret})
    except:
        print(
            f"[ { bcolors.BOLD}SOCKET{bcolors.RESET} ] Can't connect socket IO to {URL}...")
        exit(1)
    else:
        print(
            f"[ { bcolors.BOLD}SOCKET{bcolors.RESET} ] Connect socket success fully!")


def getQueue():
    db.update()
    cur = db.query(
        """SELECT * FROM submission as S
            LEFT JOIN problem as B ON S.problemId = B.id
            WHERE status = 'waiting' ORDER BY creationDate"""
    )
    data = cur.fetchone()
    cur.close()
    return data


def getQueueById(submissionId):
    db.update()
    cur = db.query(
        """SELECT * FROM submission as S
        LEFT JOIN problem as B ON S.problemId = B.id
        WHERE S.id = %s""", (str(submissionId),))
    data = cur.fetchone()
    cur.close()
    return data


def updateRunningInCase(resultId, case, userID):
    sql = "UPDATE submission SET result = %s, updateDate = %s, status = 'grading' WHERE id = %s"
    verdictText = f"Running in testcase {case+1}"
    val = (verdictText, datetime.now(), str(resultId))
    cur = db.query(sql, val)
    cur.close()
    db.update()
    if socketIO.connected:
        socketIO.emit("grader-to-server",
                      [resultId, verdictText, 0, 0, "grading", "", userID])


def updateResult(resultId, result, score, sumTime, errmsg, userID):
    sql = """UPDATE submission SET result = %s, score = %s, timeUsed = %s,
            status = %s, errmsg = %s, updateDate = %s WHERE id = %s"""
    status = "accept" if all(c in "P[]" for c in result) else "reject"
    val = (result, score, int(sumTime), status,
           errmsg, datetime.now(), str(resultId))
    cur = db.query(sql, val)
    cur.close()
    db.update()
    if socketIO.connected:
        socketIO.emit("finish-sub")
        socketIO.emit("grader-to-server",
                      [resultId, result, score, sumTime, status, errmsg, userID])


def closeConnection():
    db.disconnect()


# from .dbInit import init
# from datetime import datetime


# db = init()
# cursor = db.cursor(buffered=True)


# def getQueue():
#     update()
#     cursor.execute(
#         '''SELECT * FROM submission as S
#             LEFT JOIN problem as B ON S.problemId = B.id
#             WHERE status = 'waiting' ORDER BY creationDate'''
#     )
#     return cursor.fetchone()


# def updateRunningInCase(resultId, case):
#     sql = "UPDATE submission SET result = %s, updateDate = %s, status = 'grading' WHERE id = %s"
#     val = (f'''Running in testcase {case+1}''', datetime.now(), str(resultId))
#     cursor.execute(sql, val)
#     update()


# def updateResult(resultId, result, score, mxScore, sumTime, errmsg):
#     sql = '''UPDATE submission SET result = %s, score = %s, timeUsed = %s,
#             status = %s, errmsg = %s, updateDate = %s WHERE id = %s'''
#     status = 'accept' if (int(score) == mxScore) else 'reject'
#     val = (result, score, int(sumTime),
#            status, errmsg, datetime.now(), str(resultId))
#     cursor.execute(sql, val)
#     update()


# def update():
#     db.commit()


# def closeConnection():
#     db.close()
