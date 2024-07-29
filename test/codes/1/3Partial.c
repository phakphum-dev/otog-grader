/*
mode : classic
expected : PPPPP----P
score : 60
*/
#include <stdio.h>
#include <stdlib.h>
int main() {
    int a, b;scanf("%d %d", &a, &b);
    if (a > 100) {
        a = 100;
    }
    if (b > 100) {
        b = 100;
    }
    printf("%d", a + b);
}