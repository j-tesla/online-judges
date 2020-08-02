/*
*   author: @j-tesla
*/

// C++14

#pragma GCC optimize ("O3")
#pragma GCC target ("sse4")

#include <bits/stdc++.h>

using namespace std;

#define uns unsigned
typedef long long ll;
typedef vector<bool> vb;
typedef vector<char> vc;
typedef vector<int> vi;
typedef pair<int, int> ii;
typedef vector<uns> vu;
typedef vector<long> vl;

#define din(x) int x; cin >> x;
#define in(x) cin >> x;
#define full(x) x.begin(), x.end()

#define eb emplace_back
#define ins insert
#define f first
#define s second


int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    din(t)
    while (t--) {
        din(n)
        int s = 0;
        while (n > 0) {
            n /= 5;
            s += n;
        }
        cout << s << endl;
    }
    return 0;
}