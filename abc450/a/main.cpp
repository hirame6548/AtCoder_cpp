#include <bits/stdc++.h>
using namespace std;

#define rep(i, n) for (int i = 0; i < (int)(n); i++)
#define rep2(i, a, b) for (int i = (a); i < (int)(b); i++)
#define all(v) v.begin(), v.end()
using ll = long long;

// vectorの入力を cin >> A で行う (vector<int> A(N); と宣言しておく)
template <typename T>
istream& operator>>(istream& is, vector<T>& v) {
    for (auto& x : v) is >> x;
    return is;
}

// vectorの出力を cout << A で行う
template <typename T>
ostream& operator<<(ostream& os, const vector<T>& v) {
    for (int i = 0; i < (int)v.size(); i++) {
        os << v[i] << (i == (int)v.size() - 1 ? "" : " ");
    }
    return os;
}



int main() {
    cin.tie(nullptr);
    ios_base::sync_with_stdio(false);
    
    
    int N;
    cin >> N;

    rep(i, N) {
        if (i != N-1) {
            cout << N-i << ",";
        }
        else {
            cout << N-i << "\n";
        }
    }


    return 0;
}
