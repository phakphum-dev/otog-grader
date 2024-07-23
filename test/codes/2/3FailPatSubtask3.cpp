/*
mode : classic
expected : (PPPPP)[PPPP][PP-](PP)(SS)
score : 53
*/
#include <iostream>

int main() {
    int subtask, caseNumber;
    std::cin >> subtask >> caseNumber;

    if (subtask == 3 && caseNumber > 2) {
        std::cout << "Fail";
    }

    std::cout << 'P';
}