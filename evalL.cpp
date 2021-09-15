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
    for(int i = 0; i < SIZE; i++)
    {
        if(isPrime(i) && inp[i] == 1)
        {
            fitness += 1;
        }
        else if(!isPrime(i) && inp[i] == 0)
        {
            fitness += 1;
        }
    }
    return fitness;
}