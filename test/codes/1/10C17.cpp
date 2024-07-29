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
    int arr[2] = { a, b };
    auto [x, y] = arr;
    std::cout << x + y;
}
