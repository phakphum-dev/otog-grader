import time
from constants.colors import colors
from .dbInit import DB
from datetime import datetime
import traceback

db = DB()


def testDBConnection():
    try:
        db.connect()
    except Exception:
        print(f"{colors.FAIL}[ MYSQL ]{colors.RESET} Connection failed.")
        traceback.print_exc()
        exit(1)
    print(
        f"{colors.OKGREEN}[ MYSQL ]{colors.RESET} Connect MYSQL success fully!.")
    DBDisconnect()


def DBConnect():
    try:
        db.connect()
    except:
        for i in range(5):
            try:
                print(
                    f"{colors.WARNING}[ MYSQL ]{colors.RESET} Connection failed, retrying in ({i+1}) secs..."
                )
                time.sleep(i + 1)
                db.connect()
                print(
                    f"{colors.OKGREEN}[ MYSQL ]{colors.RESET} Connect MYSQL success fully!.")
                return
            except:
                pass
        print(
            f"{colors.FAIL}[ MYSQL ]{colors.RESET} Connection Lost.")
        exit(1)


def DBDisconnect():
    db.disconnect()


def getQueue():
    db.update()
    cur = db.query(
        """SELECT * FROM submission as S
            LEFT JOIN problem as B ON S.problemId = B.id
            WHERE status = 'waiting' ORDER BY creationDate"""
    )
    result = cur.fetchone()
    cur.close()
    return result


def updateRunningInCase(resultId, case):
    sql = "UPDATE submission SET result = %s, updateDate = %s, status = 'grading' WHERE id = %s"
    val = (f"Running in testcase {case+1}", datetime.now(), str(resultId))
    cur = db.query(sql, val)
    cur.close()
    db.update()


def updateResult(resultId, result, score, sumTime, errmsg):
    sql = """UPDATE submission SET result = %s, score = %s, timeUsed = %s, 
            status = %s, errmsg = %s, updateDate = %s WHERE id = %s"""
    status = "accept" if all(
        c in "P[]()" for c in result) or result == "Accepted" else "reject"
    val = (result, score, int(sumTime), status,
           errmsg, datetime.now(), str(resultId))
    cur = db.query(sql, val)
    cur.close()
    db.update()
