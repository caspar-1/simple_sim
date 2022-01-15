#include <iostream>
#include <valarray>
#include <chrono>
using namespace std::chrono;


typedef std::valarray<float> T;


 
int main(void)
{
    uint32_t sz=100000000;
    
    T* p=new T(sz);

    auto start = high_resolution_clock::now();
    *p+=1;
    *p*=2;
    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<nanoseconds>(stop - start);
    std::cout << "ran :"<<sz << " in " << duration.count() / 1000 << " uS [ " << duration.count() /(float)sz << " nS/iteration ]" << std::endl;


    delete p;
    return 0;
}