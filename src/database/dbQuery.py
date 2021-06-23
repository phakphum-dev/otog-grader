from .dbInit import DB
from datetime import datetime
import time
import socketio

db = DB()
bigSocket = socketio.Client()


def testConnection():
    db.connect()


def socketTestConnect():
    try:
        print("Connect to server...")
        time.sleep(2)
        bigSocket.connect('192.168.0.7:8000')
    except:
        print("Can't connect socket IO...")
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


def updateRunningInCase(resultId, case):
    sql = "UPDATE submission SET result = %s, updateDate = %s, status = 'grading' WHERE id = %s"
    val = (f"Running in testcase {case+1}", datetime.now(), str(resultId))
    cur = db.query(sql, val)
    db.update()


def updateResult(resultId, result, score, sumTime, errmsg, userID):
    sql = """UPDATE submission SET result = %s, score = %s, timeUsed = %s, 
            status = %s, errmsg = %s, updateDate = %s WHERE id = %s"""
    status = "accept" if all(c in "P[]" for c in result) else "reject"
    val = (result, score, int(sumTime), status,
           errmsg, datetime.now(), str(resultId))
    cur = db.query(sql, val)
    db.update()
    bigSocket.emit("garger-to-server",
                   [resultId, result, score, sumTime, errmsg, userID])


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
