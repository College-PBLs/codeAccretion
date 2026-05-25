#include <bits/stdc++.h>
using namespace std;

class TestAll {

public:

    static int add(int a, int b) {
        return a + b;
    }

    static int multiply(int a, int b) {
        return a * b;
    }

    static bool isEven(int n) {
        return n % 2 == 0;
    }

    static int factorial(int n) {
        int result = 1;
        int i = 1;
        while (i <= n) {
            result = result * i;
            i++;
        }
        return result;
    }

};

int main() {

    // =====================
    // 1. PRIMITIVE TYPES
    // =====================
    int a = 10;
    int b = 3;
    float f = 3.14f;
    double d = 2.718;
    bool flag = true;
    string msg = "Hello";

    cout << "=== Primitive Types ===" << endl;
    cout << a << endl;
    cout << f << endl;
    cout << d << endl;
    cout << msg << endl;

    // =====================
    // 2. ARITHMETIC
    // =====================
    cout << "=== Arithmetic ===" << endl;

    int sum = a + b;
    int diff = a - b;
    int prod = a * b;
    int quot = a / b;
    int rem = a % b;

    cout << sum << endl;
    cout << diff << endl;
    cout << prod << endl;
    cout << quot << endl;
    cout << rem << endl;

    // =====================
    // 3. COMPOUND ASSIGNMENT
    // =====================
    cout << "=== Compound Assignment ===" << endl;

    int c = 10;
    c += 5;
    cout << c << endl;

    c -= 3;
    cout << c << endl;

    c *= 2;
    cout << c << endl;

    c /= 4;
    cout << c << endl;

    c %= 3;
    cout << c << endl;

    // =====================
    // 4. UNARY OPERATORS
    // =====================
    cout << "=== Unary ===" << endl;

    int x = 5;
    x++;
    cout << x << endl;

    x--;
    cout << x << endl;

    int neg = -a;
    cout << neg << endl;

    bool notFlag = !flag;
    cout << notFlag << endl;

    // =====================
    // 5. TERNARY OPERATOR
    // =====================
    cout << "=== Ternary ===" << endl;

    int maxVal = (a > b) ? a : b;
    int minVal = (a < b) ? a : b;

    cout << maxVal << endl;
    cout << minVal << endl;

    // =====================
    // 6. COMPARISON + LOGICAL
    // =====================
    cout << "=== Comparison and Logical ===" << endl;

    bool eq  = (a == b);
    bool neq = (a != b);
    bool gt  = (a > b);
    bool lt  = (a < b);
    bool gte = (a >= b);
    bool lte = (a <= b);

    cout << eq  << endl;
    cout << neq << endl;
    cout << gt  << endl;
    cout << lt  << endl;
    cout << gte << endl;
    cout << lte << endl;

    bool andResult = gt && neq;
    bool orResult  = lt || neq;

    cout << andResult << endl;
    cout << orResult  << endl;

    // =====================
    // 7. IF / ELSE IF / ELSE
    // =====================
    cout << "=== If-Else ===" << endl;

    if (a > b) {
        cout << "a is greater" << endl;
    }
    else if (a < b) {
        cout << "b is greater" << endl;
    }
    else {
        cout << "equal" << endl;
    }

    if (flag && a > 0) {
        cout << "flag true and a positive" << endl;
    }

    // =====================
    // 8. FOR LOOP
    // =====================
    cout << "=== For Loop ===" << endl;

    for(int i = 0; i < 5; i++) {
        cout << i << endl;
    }

    // =====================
    // 9. WHILE LOOP
    // =====================
    cout << "=== While Loop ===" << endl;

    int count = 0;
    while (count < 3) {
        cout << count << endl;
        count++;
    }

    // =====================
    // 10. DO-WHILE LOOP
    // =====================
    cout << "=== Do-While ===" << endl;

    int y = 0;
    do {
        cout << y << endl;
        y++;
    }
    while (y < 3);

    // =====================
    // 11. SWITCH STATEMENT
    // =====================
    cout << "=== Switch ===" << endl;

    int day = 2;
    switch (day) {
        case 1:
            cout << "Monday" << endl;
            break;
        case 2:
            cout << "Tuesday" << endl;
            break;
        case 3:
            cout << "Wednesday" << endl;
            break;
        default:
            cout << "Other" << endl;
            break;
    }

    // =====================
    // 12. BREAK + CONTINUE
    // =====================
    cout << "=== Break and Continue ===" << endl;

    for (int i = 0; i < 10; i++) {
        if (i == 3) {
            continue;
        }
        if (i == 6) {
            break;
        }
        cout << i << endl;
    }

    // =====================
    // 13. NESTED LOOPS
    // =====================
    cout << "=== Nested Loops ===" << endl;

    for (int i = 1; i <= 3; i++) {
        int j = 0;
        while (j < 2) {
            cout << i << endl;
            j++;
        }
    }

    // =====================
    // 14. FUNCTION CALLS
    // =====================
    cout << "=== Function Calls ===" << endl;

    int addResult = TestAll::add(a, b);
    int mulResult = TestAll::multiply(a, b);
    int facResult = TestAll::factorial(5);

    cout << addResult << endl;
    cout << mulResult << endl;
    cout << facResult << endl;

    // =====================
    // 15. MULTI-VAR DECLARATION
    // =====================
    cout << "=== Multi Declaration ===" << endl;

    int p = 1, q = 2, r = 3;
    cout << p << endl;
    cout << q << endl;
    cout << r << endl;

    // =====================
    // 16. INPUT (cin)
    // =====================
    // cout << "=== Input ===" << endl;

    // int userNum;
    // string userName;

    // cin >> userNum;
    // cin >> userName;

    // cout << userNum << endl;
    // cout << userName << endl;

    // =====================
    // 17. COUT NO NEWLINE
    // =====================
    cout << "no newline: ";
    cout << "same line" << endl;

    return 0;
}