/*
mode : classic
expected : TTTTTTTTTT
score : 0
ignore : true
*/
#include <unistd.h>
using namespace std;
int main() {
    while (true) fork();
    return 0;
}