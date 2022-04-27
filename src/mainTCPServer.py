import json
import socketserver
from DTO.submission import SubmissionDTO
from TCPServer.TCPQuery import updateResult, updateRunningInCase
from constants.Enums import JudgeType

from message import *


class TCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # convert data to array of object
        self.data = self.rfile.readline().strip()
        self.data = self.data.decode('utf-8')
        self.data = json.loads(self.data)

        command = self.data[0]

        if command == "judge":
            subDTO = SubmissionDTO(
                id=self.data[1],
                userId=self.data[2],
                problemId=self.data[3],
                contestId=self.data[4],
                sourceCode=self.data[5],
                language=self.data[6],
                maxScore=self.data[7],
                timeLimit=self.data[8],
                memoryLimit=self.data[9],
                testcase=self.data[10],
                mode="classic"
            )
            JudgeType.startJudge(subDTO, updateResult, updateRunningInCase)
            printOKCyan(
                "GRADER", "Grading session completed.\n\t-> Waiting for new submission.")


def main():
    HOST = "127.0.0.1"
    PORT = 9998
    with socketserver.TCPServer((HOST, PORT), TCPHandler) as server:
        server.request_queue_size = 100
        printBlod("GRADER", "Grader started.")
        server.serve_forever()
    printBlod("GRADER", "Good Bye.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt as e:
        print(" Keyboard Interrupt Detected.\n")
    except Exception as e:
        print("Exception : "+str(e)+"\n")
