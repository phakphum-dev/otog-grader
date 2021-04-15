from .dbInit import DB
from datetime import datetime

db = DB()


def testConnection():
    db.connect()


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


def updateResult(resultId, result, score, sumTime, errmsg):
    sql = """UPDATE submission SET result = %s, score = %s, timeUsed = %s, 
            status = %s, errmsg = %s, updateDate = %s WHERE id = %s"""
    status = "accept" if all(c in "P[]" for c in result) else "reject"
    val = (result, score, int(sumTime), status, errmsg, datetime.now(), str(resultId))
    cur = db.query(sql, val)
    db.update()


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
