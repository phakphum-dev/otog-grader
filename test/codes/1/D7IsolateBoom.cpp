/*
mode : classic
expected : XXXXXXXXXX
score : 0
ignore : true
*/
#include <iostream>
#include <bits/stdc++.h>
using namespace std;
int arr[100];

int main() {
    int n, m; int number;
    n = 100000; m = 100000;
    for (int i = 0; i < n; i++) {
        arr[n] = i;
    }
    sort(arr, arr + n);
    for (int j = 0; j < n; j++) {
        cout << arr[j];
        if (j != n) cout << " ";
    }
    return 0;
}