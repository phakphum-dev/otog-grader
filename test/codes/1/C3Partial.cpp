/*
mode : codeforces
expected : Wrong answer on pretest 6
score : 0
*/
#include <iostream>

int main() {
    int a, b;
    std::cin >> a >> b;
    if (a > 100) a = 100;
    if (b > 100) b = 100;
    std::cout << a + b;
}