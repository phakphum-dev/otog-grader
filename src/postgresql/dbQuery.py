import time
from DTO.result import ResultDTO
from DTO.submission import SubmissionDTO
from DTO.contest import ContestMode, ContestScoreDTO, ContestScoreHistoryDTO
from constants.colors import colors
from .dbInit import DB
from datetime import datetime
import traceback
import json

db = DB()


def testDBConnection():
    try:
        db.connect()
    except Exception:
        print(f"{colors.FAIL}[ PostgreSQL ]{colors.RESET} Connection failed.")
        traceback.print_exc()
        exit(1)
    print(
        f"{colors.OKGREEN}[ PostgreSQL ]{colors.RESET} Connect PostgreSQL success fully!.")
    DBDisconnect()


def DBConnect():
    try:
        db.connect()
    except:
        for i in range(5):
            try:
                print(
                    f"{colors.WARNING}[ PostgreSQL ]{colors.RESET} Connection failed, retrying in ({i+1}) secs..."
                )
                time.sleep(i + 1)
                db.connect()
                print(
                    f"{colors.OKGREEN}[ PostgreSQL ]{colors.RESET} Connect PostgreSQL success fully!.")
                return
            except:
                pass
        print(
            f"{colors.FAIL}[ PostgreSQL ]{colors.RESET} Connection Lost.")
        exit(1)


def DBDisconnect():
    db.disconnect()

def getQueueModBalace(nGrader:int, thisGrader:int):
    #thisGrader will count from 1 to nGrader
    db.update()
    cur = db.query(
        f"""SELECT S.*, B."timeLimit", B."memoryLimit", B."case", B."score" as "maxScore" FROM submission as S
            LEFT JOIN problem as B ON S."problemId" = B."id"
            WHERE status = 'waiting' AND mod(S.id,{nGrader}) = {thisGrader - 1} ORDER BY S."creationDate" """
    )
    result = cur.fetchone()
    cur.close()
    return result

def getQueue():
    db.update()
    cur = db.query(
        f"""SELECT S.*, B."timeLimit", B."memoryLimit", B."case", B."score" as "maxScore" FROM submission as S
            LEFT JOIN problem as B ON S."problemId" = B."id"
            WHERE status = 'waiting' ORDER BY S."creationDate" """
    )
    result = cur.fetchone()
    cur.close()
    return result


def initContestScore(contestId, userId, problemId, submissionId):
    sql = """SELECT id, score FROM "contestScore" WHERE
        "contestId" = %s AND
        "userId" = %s AND
        "problemId" = %s"""
    val = (contestId, userId, problemId)
    cur = db.query(sql, val)
    contestScoreId = -1
    score = 0
    if cur.rowcount == 0:
        sql = """INSERT INTO "contestScore" ("contestId", "userId", "problemId", score)
                VALUES (%s, %s, %s, 0) RETURNING id"""
        val = (contestId, userId, problemId)
        cur = db.query(sql, val)
        contestScoreId = cur.fetchone().id
    else:
        result = cur.fetchone()
        contestScoreId = result.id
        score = result.score
    cur.close()
    db.update()
    sql = """SELECT * FROM "contestScoreHistory" WHERE "submissionId" = %s"""
    val = (submissionId,)
    cur = db.query(sql, val)
    if cur.rowcount == 0:
        sql = """INSERT INTO "contestScoreHistory" ("contestScoreId", "submissionId", score)
                VALUES (%s, %s, 0)"""
        val = (contestScoreId, submissionId)
        cur = db.query(sql, val)
    cur.close()
    db.update()
    history = []
    sql = """SELECT "submissionId", score FROM "contestScoreHistory" WHERE "contestScoreId" = %s"""
    val = (contestScoreId,)
    cur = db.query(sql, val)
    for row in cur.fetchall():
        history.append(ContestScoreHistoryDTO(submissionId = row.submissionId, score = row.score))
    history.sort(key = lambda x: x.submissionId)
    cur.close()
    return ContestScoreDTO(
        id = contestScoreId,
        score = score,
        history = history
    )


def getContestMode(contestId):
    sql = """SELECT "gradingMode" FROM contest WHERE id = %s"""
    val = (contestId,)
    cur = db.query(sql, val)
    result = cur.fetchone()
    cur.close()
    return ContestMode(result.gradingMode)


def getSubmissionScore(submissionId):
    sql = """SELECT score FROM "submissionResult" WHERE "submissionId" = %s"""
    val = (submissionId,)
    cur = db.query(sql, val)
    result = cur.fetchone()
    cur.close()
    return result.score


def getSubtaskScores(submissionId):
    sql = """SELECT id FROM "submissionResult" WHERE "submissionId" = %s"""
    val = (submissionId,)
    cur = db.query(sql, val)
    result = cur.fetchone()
    cur.close()
    submissionResultId = result.id
    sql = """SELECT score FROM "subtaskResult" WHERE "submissionResultId" = %s ORDER BY "subtaskIndex" """
    val = (submissionResultId,)
    cur = db.query(sql, val)
    scores = []
    for row in cur.fetchall():
        scores.append(row.score)
    cur.close()
    return scores


def updateHistory(sql, val, history: ContestScoreHistoryDTO, score):
    if history.score != score:
        sql += ["""UPDATE "contestScoreHistory" SET score = %s WHERE "submissionId" = %s"""]
        val += [score, history.submissionId]


def updateContestScore(submission: SubmissionDTO, result: ResultDTO):
    db.update()
    contestId = submission.contestId
    userId = submission.userId
    problemId = submission.problemId
    contestMode = getContestMode(contestId)
    contestScore = initContestScore(contestId, userId, problemId, submission.id)

    sql = []
    val = []

    score = 0
    lastSubmissionId = -1

    if contestMode == ContestMode.BEST_SUBMISSION:
        for history in contestScore.history:
            new_score = getSubmissionScore(history.submissionId)
            if new_score > score:
                score = new_score
                lastSubmissionId = history.submissionId
            updateHistory(sql, val, history, score)

    elif contestMode == ContestMode.BEST_SUBTASK:
        subtaskScores = []
        for history in contestScore.history:
            while len(subtaskScores) < len(result.fullResult):
                subtaskScores.append(0)
            subtaskScores = [max(subtaskScores[i], score) for i, score in enumerate(getSubtaskScores(history.submissionId))]
            new_score = sum(subtaskScores)
            if new_score > score:
                score = new_score
                lastSubmissionId = history.submissionId
            updateHistory(sql, val, history, score)

    else: # Default: Lastest Submission
        for history in contestScore.history:
            score = getSubmissionScore(history.submissionId)
            lastSubmissionId = history.submissionId
            updateHistory(sql, val, history, score)

    sql += ["""UPDATE "contestScore" SET score = %s WHERE id = %s"""]
    val += [score, contestScore.id]
    
    if lastSubmissionId != submission.id:
        sql += ["""UPDATE "contestScore" CS 
                SET score = %s, "latestSubmission" = S."creationDate" 
                FROM submission S 
                WHERE CS.id = %s AND S.id = %s"""]
        val += [score, contestScore.id, submission.id]

    cur = db.query(";".join(sql), tuple(val))
    cur.close()

    db.update()


def updateRunningInCase(resultId, case):
    sql = """UPDATE submission SET "updateDate" = %s, status = 'grading' WHERE id = %s"""
    val = (datetime.now(), str(resultId))
    cur = db.query(sql, val)
    cur.close()
    db.update()


def updateResult(result: ResultDTO):
    currentDate = datetime.now()
    sql = ["""UPDATE submission SET status = %s, "updateDate" = %s WHERE id = %s"""]
    val = [result.status.value, currentDate, result.id]
    sql += ["""INSERT INTO "submissionResult" ("submissionId", result, score, "timeUsed", "memUsed", errmsg)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id"""]
    val += [result.id, result.result, result.score, result.sumTime, result.memUse, result.errmsg]
    cur = db.query(";".join(sql), tuple(val))
    submissionResultId = cur.fetchone().id
    cur.close()
    subtaskIndex = 0
    for subtask in result.fullResult:
        subtaskIndex += 1
        sql = ["""INSERT INTO "subtaskResult" ("submissionResultId", "subtaskIndex", score, "fullScore")
                VALUES (%s, %s, %s, %s) RETURNING id"""]
        val = [submissionResultId, subtaskIndex, subtask.score, subtask.fullScore]
        cur = db.query(";".join(sql), tuple(val))
        subtaskResultId = cur.fetchone()
        cur.close()
        testcaseIndex = 0
        sql = []
        val = []
        for verdict in subtask.verdicts:
            testcaseIndex += 1
            sql += ["""INSERT INTO verdict ("subtaskId", "testcaseIndex", status, percent, "timeUsed", "memUsed")
                    VALUES (%s, %s, %s, %s, %s, %s)"""]
            val += [subtaskResultId, testcaseIndex, verdict.status.value, verdict.percent, verdict.timeUse, verdict.memUse]
        cur = db.query(";".join(sql), tuple(val))
        cur.close()
    db.update()
