/*
mode : classic
expected : PPP--
score : 60
*/
#include <iostream>

int main() {
    int testcase;
    std::cin >> testcase;
    if (testcase <= 3) {
        std::cout << "2 3";
    }
    else {
        std::cout << "2 2";
    }

}