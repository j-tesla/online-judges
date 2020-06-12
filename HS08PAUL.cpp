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
typedef pair<int,int> ii;
typedef vector<uns> vu;
typedef vector<long> vl;

#define din(x) int x; cin >> x;
#define in(x) cin >> x;
#define full(x) x.begin(), x.end()

#define eb emplace_back
#define ins insert
#define f first
#define s second

const int N = 10000000;

int form(int i, int j) {
    return i * i + j * j * j * j;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int sqrtN = sqrt(N);

    vb is_prime(N + 1, true);
    is_prime[0] = is_prime[1] = false;              // 0 and 1 aren't primes

    for (int i = 2; i <= sqrtN; ++i) {
        if (is_prime[i]) {
            for (int j = i * i; j <= N; j += i) {
                is_prime[j] = false;
            }
        }
    }

    return 0;
}