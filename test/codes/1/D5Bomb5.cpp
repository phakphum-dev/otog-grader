/*
mode : classic
expected : -----XX-X-
score : 0
*/
#include<bits/stdc++.h>
using namespace std;
using lli = long long;
using pii = pair<int, int>;

#define sz(x) x.size()
#define all(x) x.begin(), x.end()

#define rep(i, begin, end) for (__typeof(end) i = (begin) - ((begin) > (end)); i != (end) - ((begin) > (end)); i += 1 - 2 * ((begin) > (end)))

#define dbg(args...) { string _s = #args; replace(_s.begin(), _s.end(), ',', ' '); stringstream _ss(_s); istream_iterator<string> _it(_ss); err(_it, args); }

void err(istream_iterator<string> it) {}
template<typename T, typename... Args>
void err(istream_iterator<string> it, T a, Args... args) {
    cerr << *it << '=' << a << endl;
    err(++it, args...);
}

#define input() (*istream_iterator<int>(cin))
#define strin() (*istream_iterator<string>(cin))

const int mxn = 1e5;
vector<int> adj[mxn];
int main() {
    //ios::sync_with_stdio(false);
    //freopen("10.in", "r", stdin);
    int n = input();
    rep(i, 0, n) {
        int u = input(), v = input();
        rep(j, 0, n) adj[i].push_back(j);
    }
    cout << "OTOG IS LOVE";
    return 0;
}