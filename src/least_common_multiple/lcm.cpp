#include <iostream>
#include <numeric>

int gcd(int a, int b)
{
    for (;;)
    {
        if (a == 0) return b;
        b %= a;
        if (b == 0) return a;
        a %= b;
    }
}

int lcm(int a, int b)
{
    int temp = gcd(a, b);

    return temp ? (a / temp * b) : 0;
}

int main()
{
    int arr[] = { 5, 7, 9, 12 };

    //int result = std::accumulate(arr, arr + 4, 1, lcm);
	int result = lcm(5, 7);

    std::cout << result << '\n';
	system("pause");
}

