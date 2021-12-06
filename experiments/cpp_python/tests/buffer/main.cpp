#include <iostream>
#include "stdint.h"
#include "buffer.h"
#include "base_buffer.h"
#include <chrono>
#include <thread>



int main(void)
{
    using namespace std::complex_literals;

    std::cout << "BUILT  " << __TIME__ <<" : "<< __DATE__ <<std::endl;
    
    
    uint32_t sz = 500;

    std::complex<double>  x = 1.0 + 3.0i;

    x=x + 3.0i;
    std::cout << x << std::endl;




    BaseBuffer *a = new Buffer<float>((uint32_t)sz);
    BaseBuffer *b = new Buffer<uint32_t>((uint32_t)sz);
    BaseBuffer *c = new Buffer<std::complex<double>>((uint32_t)sz);
    BaseBuffer *d = new Buffer<double>((uint32_t)sz);

    
   


    float v = 1;
    for (uint32_t i = 0; i < sz+1; i++)
    {
        std::complex<float> f(v,1);
  
        a->addData(v);
        b->addData(v);
        c->addData(f );
        d->addData(v);

        //std::cout << i << std::endl;
        if (a->is_full())
        {
            std::cout <<"full @ "<<i << std::endl;
            break;
        }
    }
    std::cout <<"sleep...." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));

    delete a;
    delete b;
    delete c;
    delete d;

   
    return 0;
}