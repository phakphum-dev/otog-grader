#include <iostream>
#include <string>
#include <fstream>
#include <cstdlib>
#include <algorithm>
using namespace std;

std::ofstream result("grader_result.txt"); // ตัวเปิดไฟล์ "grader_result.txt"
void correct() {
    ::result << 'P'; // เขียนไฟล์นั้นว่า "P"
    ::exit(0);
}
void wrong() {
    ::result << 'W'; // เขียนไฟล์นั้นว่า "W"
    ::exit(0);
}
int main(int argc, char* argv[]) {
    std::ifstream sol(argv[1]); 	//อ่าน .sol ไฟล์จาก argv ข้อที่ 1
    std::ifstream inp(argv[2]); 	//อ่าน .in ไฟล์จาก argv ข้อที่ 2
    std::ifstream cod(argv[3]); 	//อ่าน code จากไฟล์ที่น้องส่ง จาก argv ข้อที่ 3
    std::ifstream out("output.txt");//อ่าน output ที่น้อง Output ออกมา

    int num1, num2;
    out >> num1 >> num2;

    if (num1 == 69) {//This is the secret number
        result << "Noice";
    }
    if (num1 == 37) {
        while (true)
        {
            /* code */
        }

    }
    if (num1 == 420) {//This is the secret number
        return 1;
    }

    if (num1 != num2) correct();
    else wrong();
}