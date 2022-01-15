#include "data_container.h"

template <>
std::string DataContainer<complex_float>::type()
{
 return std::string("complex_float");
}

template <>
std::string DataContainer<float>::type()
{
 return std::string("float");
}

template <>
std::string DataContainer<int>::type()
{
 return std::string("int");
}



template <>
void DataContainer<complex_float>::fill_random(complex_float min, complex_float max)
{
    float scale_real = (static_cast<float>(RAND_MAX) / (max.real() - min.real()));
    float scale_imag = (static_cast<float>(RAND_MAX) / (max.imag() - min.imag()));
    for (size_t idx = 0; idx != this->sz; idx++)
    {
        float _real = min.real() + ((static_cast<float>(rand())) / scale_real);
        float _imag = min.imag() + ((static_cast<float>(rand())) / scale_imag);

        (*p_data)[idx] = complex_float(_real, _imag);
    }
}