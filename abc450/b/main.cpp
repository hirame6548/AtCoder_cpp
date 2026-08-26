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

    vector<vector<int>> grid(N, vector<int>(N, 0));

    int c;
    rep(i, N) {
        rep(j, N-i-1) {
            cin >> c;
            grid[i][i+j+1] = c;
            //cout << i << i+j+1 << "\n";
        }
    }

    auto frag = false;
    rep(i, N) {
        rep(j, N-i-1) {
            rep(k, N-i-j-2) {
                //cout << i << i+j+1 << i+j+k+2 << "\n";
                if (grid[i][i+j+1] + grid[i+j+1][i+j+k+2] < grid[i][i+j+k+2]) {
                    frag = true;
                    break;
                }
            }
            if (frag) {
                break;
            }
        }
        if (frag) {
            break;
        }
    }

    if (frag) {
        cout << "Yes" << "\n";
    } else {
        cout << "No" << "\n";
    }


    return 0;
}
