from .dbInit import DB
from datetime import datetime
import time
import socketio
import configparser

db = DB()
socketIO = socketio.Client()


def testConnection():
    db.connect()


def socketTestConnect():

    configINI = configparser.ConfigParser()
    try:
        configINI.read("./BigConfig.ini")
    except:
        print("BigConfig.ini not found...")
        exit(1)

    try:
        URL = configINI["socket"]["URL"]
        secret = configINI["socket"]["secret"]
        keySocket = configINI["socket"]["keySocket"]
    except:
        print("BigConfig.ini wrong format or missing...")
        print(
            'EG.\n[socket]\nURL = "localhost:69"\nsecret = "xxxxxxxxxxxx"\nkeySocket = "dasasdasd"')

    try:
        print("Connect to server...")
        time.sleep(2)
        socketIO.connect(URL, header={'key': keySocket}, auth=secret)
    except:
        print(f"Can't connect socket IO to {URL}...")
        exit(1)
    else:
        print("Connect socket success fully!")


def getQueue():
    db.update()
    cur = db.query(
        """SELECT * FROM submission as S
            LEFT JOIN problem as B ON S.problemId = B.id
            WHERE status = 'waiting' ORDER BY creationDate"""
    )
    return cur.fetchone()


def updateRunningInCase(resultId, case, userID):
    sql = "UPDATE submission SET result = %s, updateDate = %s, status = 'grading' WHERE id = %s"
    verdictText = f"Running in testcase {case+1}"
    val = (verdictText, datetime.now(), str(resultId))
    cur = db.query(sql, val)
    db.update()
    socketIO.emit("garger-to-server",
                  [resultId, verdictText, 0, 0, "grading", "", userID])


def updateResult(resultId, result, score, sumTime, errmsg, userID):
    sql = """UPDATE submission SET result = %s, score = %s, timeUsed = %s, 
            status = %s, errmsg = %s, updateDate = %s WHERE id = %s"""
    status = "accept" if all(c in "P[]" for c in result) else "reject"
    val = (result, score, int(sumTime), status,
           errmsg, datetime.now(), str(resultId))
    cur = db.query(sql, val)
    db.update()
    socketIO.emit("garger-to-server",
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
