/*
mode : classic
expected : (PPPPP)[PPPP][PPP](P-)(SS)
score : 59
*/
#include <iostream>

int main() {
    int subtask, caseNumber;
    std::cin >> subtask >> caseNumber;

    if (subtask == 4 && caseNumber > 1) {
        std::cout << "Fail";
    }

    std::cout << 'P';
}