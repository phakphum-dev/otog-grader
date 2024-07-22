/*
mode : classic
expected : ---------T
score : 0
ignore : true
*/
#include<bits/stdc++.h>
using namespace std;
using lli = long long;
using pii = pair<int, int>;

#define rep(i,k,n) for(int i=(k); i != int(n); ++i)
#define sz(x) x.size()
#define all(x) x.begin(), x.end()

#define dbg(x) cerr << #x << '=' << x << '\n'
#define dbg2(x, y) cerr << #x << '=' << x << ' ' << #y << '=' << y << '\n' 

#define input() (*istream_iterator<int>(cin))
#define strin() (*istream_iterator<string>(cin))

const int mxn = 13000;
struct point {
    int x, y;
};
vector<point> city;
vector<bool> flag(mxn, false);
vector<int> sum(mxn, 0);

int dist(point a, point b) {
    return max(abs(a.x - b.x), abs(a.y - b.y));
}

int find_max(int n) {
    int mx = -1, idx;
    rep(i, 0, n) {
        if (sum[i] > mx and not flag[i]) {
            mx = sum[i];
            idx = i;
        }
    }
    return idx;
}
// bool cmp(int l. )
int prim_mst(int n) {
    int fan_gain, cur, ans = 0;
    rep(cnt, 0, n - 1) {
        cur = find_max(n);
        flag[cur] = true;
        rep(nx, 0, n) {
            fan_gain = dist(city[cur], city[nx]);
            if (not flag[nx] and fan_gain > sum[nx])
                sum[nx] = fan_gain;
        }
    }
    ans = accumulate(all(sum), 0);
    return ans;
}
int main() {
    ios::sync_with_stdio(false);
    //freopen("10.in", "r", stdin);
    //freopen("10.sol", "w", stdout);
    int n = input();
    rep(i, 0, n) city.push_back({ input(), input() });
    cout << prim_mst(n);
    return 0;
}