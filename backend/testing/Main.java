public class Main {

    // --- Helper Methods ---

    public static int add(int a, int b) {
        return a + b;
    }

    public static int multiply(int a, int b) {
        return a * b;
    }

    public static boolean isEven(int n) {
        return n % 2 == 0;
    }

    public static int factorial(int n) {
        int result = 1;
        int i = 1;
        while (i <= n) {
            result = result * i;
            i++;
        }
        return result;
    }

    public static void main(String[] args) {

        // =====================
        // 1. PRIMITIVE TYPES
        // =====================
        int a = 10;
        int b = 3;
        float f = 3.14f;
        double d = 2.718;
        boolean flag = true;
        String msg = "Hello";

        System.out.println("=== Primitive Types ===");
        System.out.println(a);
        System.out.println(f);
        System.out.println(d);
        System.out.println(msg);

        // =====================
        // 2. ARITHMETIC OPERATORS
        // =====================
        System.out.println("=== Arithmetic ===");

        int sum = a + b;
        int diff = a - b;
        int prod = a * b;
        int quot = a / b;
        int rem = a % b;

        System.out.println("a + b = " + sum);
        System.out.println("a - b = " + diff);
        System.out.println("a * b = " + prod);
        System.out.println("a / b = " + quot);
        System.out.println("a % b = " + rem);

        // =====================
        // 3. COMPOUND ASSIGNMENT
        // =====================
        System.out.println("=== Compound Assignment ===");

        int c = 10;
        c += 5;
        System.out.println(c);

        c -= 3;
        System.out.println(c);

        c *= 2;
        System.out.println(c);

        c /= 4;
        System.out.println(c);

        c %= 3;
        System.out.println(c);

        // =====================
        // 4. UNARY OPERATORS
        // =====================
        System.out.println("=== Unary ===");

        int x = 5;
        x++;
        System.out.println(x);

        x--;
        System.out.println(x);

        int neg = -a;
        System.out.println(neg);

        boolean notFlag = !flag;
        System.out.println(notFlag);

        // =====================
        // 5. TERNARY OPERATOR
        // =====================
        System.out.println("=== Ternary ===");

        int maxVal = (a > b) ? a : b;
        int minVal = (a < b) ? a : b;

        System.out.println("max = " + maxVal);
        System.out.println("min = " + minVal);

        // =====================
        // 6. COMPARISON + LOGICAL
        // =====================
        System.out.println("=== Comparison and Logical ===");

        boolean eq  = (a == b);
        boolean neq = (a != b);
        boolean gt  = (a > b);
        boolean lt  = (a < b);
        boolean gte = (a >= b);
        boolean lte = (a <= b);

        System.out.println(eq);
        System.out.println(neq);
        System.out.println(gt);
        System.out.println(lt);
        System.out.println(gte);
        System.out.println(lte);

        boolean andResult = gt && neq;
        boolean orResult  = lt || neq;

        System.out.println(andResult);
        System.out.println(orResult);

        // =====================
        // 7. IF / ELSE IF / ELSE
        // =====================
        System.out.println("=== If-Else ===");

        if (a > b) {
            System.out.println("a is greater than b");
        } else if (a < b) {
            System.out.println("b is greater than a");
        } else {
            System.out.println("a equals b");
        }

        if (flag && a > 0) {
            System.out.println("flag is true and a is positive");
        }

        // =====================
        // 8. FOR LOOP
        // =====================
        System.out.println("=== For Loop ===");

        for (int i = 0; i < 5; i++) {
            System.out.println(i);
        }

        // =====================
        // 9. WHILE LOOP
        // =====================
        System.out.println("=== While Loop ===");

        int count = 0;
        while (count < 3) {
            System.out.println(count);
            count++;
        }

        // =====================
        // 10. DO-WHILE LOOP
        // =====================
        System.out.println("=== Do-While Loop ===");

        int y = 0;
        do {
            System.out.println(y);
            y++;
        } while (y < 3);

        // =====================
        // 11. SWITCH STATEMENT
        // =====================
        System.out.println("=== Switch ===");

        int day = 2;
        switch (day) {
            case 1:
                System.out.println("Monday");
                break;
            case 2:
                System.out.println("Tuesday");
                break;
            case 3:
                System.out.println("Wednesday");
                break;
            default:
                System.out.println("Other day");
                break;
        }

        // =====================
        // 12. BREAK + CONTINUE
        // =====================
        System.out.println("=== Break and Continue ===");

        for (int i = 0; i < 10; i++) {
            if (i == 3) {
                continue;
            }
            if (i == 6) {
                break;
            }
            System.out.println(i);
        }

        // =====================
        // 13. NESTED LOOPS
        // =====================
        System.out.println("=== Nested Loops ===");

        for (int i = 1; i <= 3; i++) {
            int j = 0;
            while (j < 2) {
                System.out.println(i + j);
                j++;
            }
        }

        // =====================
        // 14. FUNCTION CALLS
        // =====================
        System.out.println("=== Function Calls ===");

        int addResult = add(a, b);
        int mulResult = multiply(a, b);
        int facResult = factorial(5);

        System.out.println(addResult);
        System.out.println(mulResult);
        System.out.println(facResult);

        // =====================
        // 15. MULTI-VAR DECLARATION
        // =====================
        System.out.println("=== Multi Declaration ===");

        int p = 1, q = 2, r = 3;
        System.out.println(p + q + r);

        // =====================
        // 16. PRINT WITHOUT NEWLINE
        // =====================
        System.out.print("no newline: ");
        System.out.println("same line");

    }
}

// public class Main {
//     public static void main(String[] args) {
//         int sum = 0;

//         for(int i = 0; i < 3; i++) {
//             sum = sum + i;
//         }

//         System.out.println(sum);
//     }
// }