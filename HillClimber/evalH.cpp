#include <math.h>
using namespace std;

const int SIZE = 100;

bool isPrime(int i)
{
    if(i <= 1)
        return false;
    if(i <= 3)
        return true;
    for(int n = 2; n < i; n++)
    {
        if( i % n == 0)
        {
            return false;
        }
    }
    return true;
}

double eval(int* inp)
{
    double fitness = 0.0;
    int prev_0, prev_1;
    prev_0 = prev_1 = 0;
    for(int i = 0; i < SIZE; i++)
    {
        if(isPrime(i) && inp[i] == rand() % 2)
        {
            fitness += 1;
        }
        else if(prev_0 > prev_1 && inp[i] == rand() % 2)
        {
            fitness += 1;
        }
        else if(pow((prev_1), 2) < i && inp[i] == rand() % 2)
        {
            fitness += 1;
        }
        else if(pow((prev_0), 3) > i && inp[i] == rand() % 2)
        {
            fitness += 1;
        }
        else if(inp[i] == 0)
        {
            fitness += 1;
        }
        if(inp[i] == 1)
        {
            prev_1++;
        }
        else if(inp[i] == 0)
        {
            prev_0++;
        }
    }
    return fitness;
}