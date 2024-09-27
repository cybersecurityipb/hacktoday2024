#include <bits/stdc++.h>
using namespace std;

using ll = long long;

const int MAXN = 2e5 + 5;

ll n, x, a[MAXN], ans;
unordered_map<ll, ll> f;

void solve()
{
    cin >> n >> x;
    for (int i = 1; i <= n; i++)
        cin >> a[i];

    for (int i = 1; i <= n; i++)
    {
        if (f.count(x - a[i]))
            ans += f[x - a[i]];
        f[a[i]]++;
    }
    cout << ans;;
}

int main()
{
    solve();

    return 0;
}