/*
mode : classic
expected : Compilation Error
score : 0
*/
#include<iostream>
#include<vector>
using namespace std;


int main() {


    int n;cin >> n;
    vector<int> data;
    set<int> ddata;

    for (int i = 0;i < n;i++) {
        int x;cin >> x;
        data.push_back(x);//O(??)
    }

    ddata.insert(3);//O(??)

    int k;cin >> k;

    int l = 0;
    int r = n - 1;


    while (l <= r) {//O(log n)
        int mid = (l + r) / 2;

        if (data[mid] == k) {
            cout << "Found yeah mann";
            break;
        }
        else if (data[mid] > k) {
            r = mid - 1;
        }
        else {
            l = mid + 1;
        }


    }







    return 0;


}
