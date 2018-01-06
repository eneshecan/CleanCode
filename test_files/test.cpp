#include <iostream>
using namespace std;

/// Checks the primality of a number and takes its square
int function(int val) {
    int i;
    bool prime = true;

    for(i = 2; i <= val / 2; ++i) {
        if(val % i == 0) {
          prime = false;
          break;
        }
    }

    if(prime)
        return val*val;
    else
        return 0;
}

int main()
{
    unsigned reslt = function(7);
    cout << "Result is " << reslt << endl;
    return 0;
}