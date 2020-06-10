/*
*   author: @j-tesla
*/

#pragma GCC optimize ("O3")
#pragma GCC target ("sse4")
 
#include <bits/stdc++.h>
 
using namespace std;

typedef long long ll;
typedef vector<bool> vb;
typedef vector<int> vi;
typedef pair<int,int> ii;
typedef vector<unsigned> vu;
typedef vector<long> vl;

#define din(x) int x; cin >> x;
#define in(x) cin >> x;
#define full(x) x.begin(), x.end()

#define eb emplace_back
#define ins insert
#define f first
#define s second

void count_primes(int n) {
    const int S = 10000;

    vector<int> primes;
    int nsqrt = sqrt(n);
    vector<char> is_prime(nsqrt + 1, true);
    for (int i = 2; i <= nsqrt; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
            for (int j = i * i; j <= nsqrt; j += i)
                is_prime[j] = false;
        }
    }

    int result = 0;
    vector<char> block(S);
    for (int k = 0; k * S <= n; k++) {
        fill(block.begin(), block.end(), true);
        int start = k * S;
        for (int p : primes) {
            int start_idx = (start + p - 1) / p;
            int j = max(start_idx, p) * p - start;
            for (; j < S; j += p)
                block[j] = false;
        }
        if (k == 0)
            block[0] = block[1] = false;
        for (int i = 0; i < S && start + i <= n; i++) {
            if (block[i]) {
                result++;
                if ( result%100 == 1)
                    cout << i + k*S << endl;
            }
        }
    }
    
}


int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    count_primes(100000000);
    return 0;
}