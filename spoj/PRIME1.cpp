/*
*   I have just solved the "Prime Generator" challenge on SPOJ - https://www.spoj.com/PRIME1 http://www.spoj.com/problems/PRIME1 #spoj #onlinejudge #problems 
*/

#pragma GCC optimize ("O3")
#pragma GCC target ("sse4")
 
#include <bits/stdc++.h>
 
using namespace std;

typedef long long ll;
typedef unsigned uns;
typedef vector<bool> vb;
typedef vector<int> vi;
typedef pair<int,int> ii;
typedef vector<uns> vu;
typedef vector<long> vl;
typedef vector<short> vs;

#define din(x) int x; cin >> x;
#define in(x) cin >> x;
#define full(x) x.begin(), x.end()

#define eb emplace_back
#define ins insert
#define f first
#define s second

vector<bool> segmentedSieve(ll L, ll R) {
    // generate all primes up to sqrt(R)
    ll lim = sqrt(R);
    vector<bool> mark(lim + 1, false);
    vector<ll> primes;
    for (ll i = 2; i <= lim; ++i) {
        if (!mark[i]) {
            primes.emplace_back(i);
            for (ll j = i * i; j <= lim; j += i)
                mark[j] = true;
        }
    }

    vector<bool> isPrime(R - L + 1, true);
    for (ll i : primes)
        for (ll j = max(i * i, (L + i - 1) / i * i); j <= R; j += i)
            isPrime[j - L] = false;
    if (L == 1)
        isPrime[0] = false;
    return isPrime;
}



int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    short t;
    in(t)
    while(t--) {
        din(m) din(n)
        vb isPrime = segmentedSieve(m, n);    

        for (auto i = 0; i < isPrime.size(); ++i) {
                
            if (isPrime[i]) {
                cout << m + i << endl;
            }
            
        }
        cout << endl;
        
    }   
    

    return 0;
}
