/*
mode : classic
expected : (PPP--)[PPPP][SSS](PP)(SS)
score : 48
*/
#include <iostream>

int main() {
    int subtask, caseNumber;
    std::cin >> subtask >> caseNumber;

    if (subtask == 1 && caseNumber > 3) {
        std::cout << "Fail";
    }

    std::cout << 'P';
}