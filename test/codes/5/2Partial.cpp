/*
mode : classic
expected : %%%%%
score : 60
*/
#include <iostream>

int num[] = { 20, 40, 64, 79, 99 };

int main() {
    int testcase;
    std::cin >> testcase;
    std::cout << num[testcase - 1];

}