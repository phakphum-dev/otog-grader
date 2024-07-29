/*
mode : classic
expected : (PPPPP)[PPPP][PPP](PP)(P-)
score : 85
*/
#include <iostream>

int main() {
    int subtask, caseNumber;
    std::cin >> subtask >> caseNumber;

    if (subtask == 5 && caseNumber > 1) {
        std::cout << "Fail";
    }

    std::cout << 'P';
}