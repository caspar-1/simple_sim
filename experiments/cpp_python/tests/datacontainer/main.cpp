#include <iostream>
#include "stdint.h"
#include "../../src/data_container.h"
#include <chrono>
#include <thread>
#include <complex>

using namespace std::chrono;

#define ITERATIONS 1000000

void math_test()
{

    std::cout << std::endl;
    std::cout << "================================================================" << std::endl;
    std::cout << "====   math_test" << std::endl;
    std::cout << "================================================================" << std::endl;
    std::cout << "BUILT  " << __TIME__ << " : " << __DATE__ << std::endl;
    auto start = high_resolution_clock::now();

    DataContainer<float> a({1.0, 2, 3, 4, 5, 6, 7, 8, 9, 10});
    DataContainer<float> b(10);
    DataContainer<float> c(1);

    b.fill_random(-10, 10);
    b.__repr__();
    c = 1.001;

    for (auto i = 0; i < ITERATIONS; i++)
    {
        a *= b / 1e5;
    }

    a[0] = 10;
    a[0]++;
    std::cout << "a[0]=" << a[0] << std::endl;

    auto stop = high_resolution_clock::now();

    auto duration = duration_cast<nanoseconds>(stop - start);

    std::cout << "Run Time:" << duration.count() / ITERATIONS << "nS/iteration" << std::endl;

    std::cout << "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" << std::endl;
    a.__repr__();
    std::cout << "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB" << std::endl;
    b.__repr__();

    std::cout << "A SUM() = " << a.sum() << std::endl;
    std::cout << "B SUM() = " << b.sum() << std::endl;
    std::cout << "C SUM() = " << c.sum() << std::endl;
    a = 1;
    b = 1;
    std::cout << "AB INNER() = " << a.dot(b) << std::endl;
}

void slice_test()
{
    std::cout << std::endl;
    std::cout << "================================================================" << std::endl;
    std::cout << "====   slice_test" << std::endl;
    std::cout << "================================================================" << std::endl;
    DataContainer<float> b(16);

    b.fill_random(-10, 10);
    b.__repr__();

    try
    {
        std::cout << "TEST: " << b.slice(0, 0).__repr__() << std::endl;
        std::cout << "TEST: " << b.slice(0, 1).__repr__() << std::endl;
        std::cout << "TEST: " << b.slice(9, 14).__repr__() << std::endl;
        std::cout << "TEST: " << b.slice(9, -2).__repr__() << std::endl;
        std::cout << "TEST: " << b.slice(9, -7).__repr__() << std::endl;
        std::cout << "TEST: " << b.slice(9, -8).__repr__() << std::endl;
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
    }
}

void complex_test()
{
    std::cout << std::endl;
    std::cout << "================================================================" << std::endl;
    std::cout << "====   complex_test" << std::endl;
    std::cout << "================================================================" << std::endl;
    DataContainer<complex_float> a(4);
    DataContainer<complex_float> b(4);
    a.fill_random(complex_float(-10, -1), complex_float(10, 1));
    b.fill_random(complex_float(-10, -1), complex_float(10, 1));
    std::cout << "A:" << a.__repr__() << std::endl;
    std::cout << "B:" << b.__repr__() << std::endl;
    a += b;
    std::cout << "A+B:" << a.__repr__() << std::endl;
    a *= complex_float(-1, 0);
    std::cout << "A+B:" << a.__repr__() << std::endl;

    std::cout << "A SUM() = " << a.sum() << std::endl;

    std::cout << "AB INNER() = " << a.dot(b) << std::endl;
}

void data_test()
{
    std::cout << std::endl;
    std::cout << "================================================================" << std::endl;
    std::cout << "====   data_test" << std::endl;
    std::cout << "================================================================" << std::endl;
    DataContainer<float> a(16);
    DataContainer<float> b(16);
    DataContainer<float> c;

    for (int i = 0; i < 16; i++)
    {
        if (i < 5)
        {
            a.push(i);
        }
        b.push((i + 1) * 2);
    }

    std::cout << "A:" << a.__repr__() << std::endl;
    std::cout << "B:" << b.__repr__() << std::endl;

    c = a + 4;
    std::cout << "A:" << c.__repr__() << std::endl;

    c = a * b;
    std::cout << "A:" << c.__repr__() << std::endl;

    c += 10;
    std::cout << "A:" << c.__repr__() << std::endl;

    c /= 10;
    std::cout << "A:" << c.__repr__() << std::endl;

    c /= b;
    std::cout << "A:" << c.__repr__() << std::endl;
}

int main(void)
{
    //math_test();
    //slice_test();
    //complex_test();
    data_test();
    return 0;
}