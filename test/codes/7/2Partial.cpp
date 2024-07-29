/*
mode : classic
expected : (P%%%%)(P%%-)(P%-)
----------- AVG    MAX   MIN
----------- ^ 26   ^ 30  ^ 0
score : 56
*/
#include <iostream>

int nums[3][5] = {
    {100, 50, 40, 30, 40},
    {100, 40, 30, 0, 0},
    {100, 20, 0, 0, 0}
};

int main() {
    int subtask, testcase;
    std::cin >> subtask >> testcase;
    std::cout << nums[subtask - 1][testcase - 1];

}