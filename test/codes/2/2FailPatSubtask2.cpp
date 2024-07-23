/*
mode : classic
expected : (PPPPP)[PPP-][PPP](SS)(SS)
score : 29
*/
#include <iostream>

int main() {
    int subtask, caseNumber;
    std::cin >> subtask >> caseNumber;

    if (subtask == 2 && caseNumber > 3) {
        std::cout << "Fail";
    }

    std::cout << 'P';
}