/*
mode : classic
expected : (P%%%%)(%%%%)(%%%)
----------- AVG    MAX   MIN
----------- ^ 26   ^ 21  ^ 6
score : 53
*/
#include <iostream>

int nums[3][5] = {
    {100, 50, 40, 30, 40},
    {20, 70, 30, 10, 0},
    {80, 40, 30, 0, 0}
};

int main() {
    int subtask, testcase;
    std::cin >> subtask >> testcase;
    std::cout << nums[subtask - 1][testcase - 1];

}