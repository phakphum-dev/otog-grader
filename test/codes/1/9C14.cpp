/*
mode : classic
expected : PPPPPPPPPP
score : 100
*/
#include <iostream>
#include <utility>

int main() {
    auto a = 0, b = 0;
    std::cin >> a >> b;
    auto p = std::make_pair(a, b);
    auto newA = std::get<0>(p);
    auto newB = std::get<1>(p);
    std::cout << newA + newB;
}