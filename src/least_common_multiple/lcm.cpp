#include <iostream>
#include <numeric>
#include <cstdlib>
#include <ctime>

using namespace std;

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
	srand(time(NULL));
	int x = rand() & 255;
	int y = rand() & 255;

	int result = lcm(x, y);

    cout << "x: " << x << ", y: " << y << ", lcm(x,y): " << result << '\n';
	system("pause");
}

