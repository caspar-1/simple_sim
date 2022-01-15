#ifndef __DATA_CONTAINER_H__
#define __DATA_CONTAINER_H__

#include <sstream>
#include <vector>
#include <memory>
#include <stdexcept>
#include <complex>
#include <string>

#define STRINGIZE(x) STRINGIZE2(x)
#define STRINGIZE2(x) #x
#define LINE_STRING STRINGIZE(__LINE__)

typedef std::complex<float> complex_float;

template <class T>
class DataContainer;

template <class T>
struct DataPointer
{
    typedef std::unique_ptr<DataContainer<T>> X;
};

template <class T>
class DataContainer
{
public:
    DataContainer();
    DataContainer(size_t sz);
    DataContainer(const DataContainer<T> &Y);
    DataContainer(std::initializer_list<T> d);
    ~DataContainer();

    void fill_random(T min = 0, T max = 1);

    static std::string type();

    bool data_is_ready();
    void clear();

    DataContainer<T> slice(int32_t start = 0, int32_t stop = 0);
    std::unique_ptr<DataContainer<T>> get_data();

    bool push(T data);
    T pop(bool &is_ok);
    void zero();
    T sum();

    DataContainer add(const T &Y);
    DataContainer add(const DataContainer<T> &Y);
    DataContainer sub(const T &Y);
    DataContainer sub(const DataContainer<T> &Y);
    DataContainer mul(const T &Y);
    DataContainer mul(const DataContainer<T> &Y);
    DataContainer div(const T &Y);
    DataContainer div(const DataContainer<T> &Y);

    T dot(const DataContainer<T> &Y);

    DataContainer<T> &operator=(const T Y);
    DataContainer<T> &operator=(const DataContainer<T> &other);

    inline const T &operator[](const uint32_t idx) const;
    inline T &operator[](const uint32_t idx);

    DataContainer operator+(const T &Y);
    DataContainer &operator+=(const T &Y);
    DataContainer operator+(const DataContainer<T> &Y);
    DataContainer &operator+=(const DataContainer<T> &Y);

    DataContainer operator-(const T &Y);
    DataContainer &operator-=(const T &Y);
    DataContainer operator-(const DataContainer<T> &Y);
    DataContainer &operator-=(const DataContainer<T> &Y);

    DataContainer &operator*=(const T &Y);
    DataContainer operator*(const T &Y);
    DataContainer &operator*=(const DataContainer<T> &Y);
    DataContainer operator*(const DataContainer<T> &Y);

    DataContainer &operator/=(const T &Y);
    DataContainer operator/(const T &Y);
    DataContainer &operator/=(const DataContainer<T> &Y);
    DataContainer operator/(const DataContainer<T> &Y);
    std::string __repr__();

    size_t get_size() { return this->sz; };
    void update_size() { this->sz = this->p_data->size(); };

    std::vector<T> *p_data;
    uint32_t write_idx;
    uint32_t rd_idx;
    size_t sz;
};

template <typename T>
DataContainer<T>::DataContainer()
{
    this->p_data = new std::vector<T>();
    this->write_idx = 0;
    this->rd_idx = 0;
    this->sz = 0;
}

template <typename T>
DataContainer<T>::DataContainer(size_t sz) : sz(sz)
{
    this->p_data = new std::vector<T>(this->sz);
    this->write_idx = 0;
    this->rd_idx = 0;
    this->zero();
}

template <typename T>
DataContainer<T>::DataContainer(const DataContainer<T> &Y)
{
    this->p_data = new std::vector<T>(Y.sz);
    this->sz = Y.sz;
    this->p_data = new std::vector<T>(this->sz);
    for (size_t idx = 0; idx < Y.sz; idx++)
    {
        (*this)[idx] = Y[idx];
    }

    this->write_idx = 0;
    this->rd_idx = 0;
}

template <typename T>
DataContainer<T>::DataContainer(std::initializer_list<T> d)
{
    this->p_data = new std::vector<T>(d);
    this->sz = p_data->size();
    this->write_idx = 0;
    this->rd_idx = 0;
}

template <typename T>
DataContainer<T>::~DataContainer()
{
    delete (this->p_data);
    this->p_data = nullptr;
    this->sz = 0;
}

template <typename T>
std::string DataContainer<T>::type()
{
    return std::string("unknown");
}

template <typename T>
void DataContainer<T>::clear()
{
    this->write_idx = 0;
    this->rd_idx = 0;
    this->zero();
}

template <typename T>
bool DataContainer<T>::data_is_ready()
{
    return (this->write_idx == this->sz);
};

template <typename T>
void DataContainer<T>::fill_random(T min, T max)
{
    T scale = (static_cast<T>(RAND_MAX) / (max - min));
    for (size_t idx = 0; idx != this->sz; idx++)
    {
        (*p_data)[idx] = min + ((static_cast<T>(rand())) / scale);
    }
}

template <typename T>
DataContainer<T> DataContainer<T>::slice(int32_t start, int32_t stop)
{
    uint32_t _start = abs(start);
    uint32_t _stop = abs(stop);
    int32_t sz = 0;

    if (stop <= 0)
    {
        sz = this->sz - _start - _stop;
    }
    else
    {
        sz = _stop - _start;
    }

    if (sz < 0)
    {
        throw std::runtime_error("incorrect slice dimensions " __FILE__ "@" LINE_STRING);
    }

    DataContainer<T> X(sz);

    for (int32_t idx = 0; idx != sz; idx++)
    {
        X[idx] = (*this->p_data)[_start + idx];
    }

    return X;
}

template <typename T>
std::unique_ptr<DataContainer<T>> DataContainer<T>::get_data()
{
    write_idx = 0;
    std::unique_ptr<DataContainer<T>> X = new DataContainer(this->sz);
    return X;
};

template <typename T>
bool DataContainer<T>::push(T data)
{
    bool err = true;
    if (sz != write_idx)
    {
        *((T *)&(this->p_data->data())[write_idx++]) = (T)data;
        err = false;
    }

    return err;
};

template <typename T>
T DataContainer<T>::pop(bool &err)
{
    T return_data = (T)0;

    if (rd_idx != write_idx)
    {
        return_data = this->p_data->at(rd_idx++);
        err = false;
    }
    else
    {
        err = true;
    }

    return return_data;
};

template <typename T>
void DataContainer<T>::zero()
{
    for (size_t idx = 0; idx != this->sz; idx++)
    {
        *((T *)&(this->p_data->data())[idx]) = (T)0;
    }
};

template <typename T>
T DataContainer<T>::sum()
{
    T _sum = 0;
    for (size_t idx = 0; idx != sz; idx++)
    {
        _sum += (*this->p_data)[idx];
    }
    return _sum;
}

template <typename T>
DataContainer<T> DataContainer<T>::add(const T &Y)
{
    DataContainer<T> res(this->sz);
    for (size_t idx = 0; idx != sz; idx++)
    {
        T x = (*this->p_data)[idx];
        res[idx] = (x + Y);
    }
    return res;
}

template <typename T>
DataContainer<T> DataContainer<T>::add(const DataContainer<T> &Y)
{
    DataContainer<T> res(this->sz);
    if (this->sz == Y.sz)
    {
        for (size_t idx = 0; idx != sz; idx++)
        {
            T x = (*this->p_data)[idx];
            T y = (*Y.p_data)[idx];

            res[idx] = (x + y);
        }
    }
    else
    {
        throw std::runtime_error("must be the same size " __FILE__ "@" LINE_STRING);
    }
    return res;
}

template <typename T>
DataContainer<T> DataContainer<T>::sub(const T &Y)
{
    DataContainer<T> res(this->sz);
    for (size_t idx = 0; idx != sz; idx++)
    {
        T x = (*this->p_data)[idx];
        res[idx] = (x - Y);
    }
    return res;
}

template <typename T>
DataContainer<T> DataContainer<T>::sub(const DataContainer<T> &Y)
{
    DataContainer<T> res(this->sz);
    if (this->sz == Y.sz)
    {
        for (size_t idx = 0; idx != sz; idx++)
        {
            T x = (*this->p_data)[idx];
            T y = (*Y.p_data)[idx];
            res[idx] = (x - y);
        }
    }
    else
    {
        throw std::runtime_error("must be the same size " __FILE__ "@" LINE_STRING);
    }
    return res;
}

template <typename T>
DataContainer<T> DataContainer<T>::mul(const T &Y)
{
    DataContainer<T> res(this->sz);
    for (size_t idx = 0; idx != sz; idx++)
    {
        T x = (*this->p_data)[idx];
        res[idx] = (x * Y);
    }
    return res;
}

template <typename T>
DataContainer<T> DataContainer<T>::mul(const DataContainer<T> &Y)
{
    DataContainer<T> res(this->sz);

    if (this->sz == Y.sz)
    {
        for (size_t idx = 0; idx != sz; idx++)
        {
            T _x = (*this->p_data)[idx];
            T _y = (*Y.p_data)[idx];

            res[idx] = (_x * _y);
        }
    }
    else
    {
        throw std::runtime_error("must be the same size " __FILE__ "@" LINE_STRING);
    }
    return res;
}

template <typename T>
DataContainer<T> DataContainer<T>::div(const T &Y)
{
    DataContainer<T> res(this->sz);

    for (size_t idx = 0; idx != sz; idx++)
    {
        T x = (*this->p_data)[idx];
        res[idx] = (x / Y);
    }
    return res;
}

template <typename T>
DataContainer<T> DataContainer<T>::div(const DataContainer<T> &Y)
{
    DataContainer<T> res(this->sz);

    if (this->sz == Y.sz)
    {
        for (size_t idx = 0; idx != sz; idx++)
        {
            T _x = (*this->p_data)[idx];
            T _y = (*Y.p_data)[idx];

            res[idx] = (_x / _y);
        }
    }
    else
    {
        throw std::runtime_error("must be the same size " __FILE__ "@" LINE_STRING);
    }
    return res;
}

template <typename T>
T DataContainer<T>::dot(const DataContainer<T> &Y)
{
    T ip = 0;

    if (this->sz == Y.sz)
    {
        DataContainer<T> X = *this;
        X.mul(Y);
        ip = X.sum();
    }
    else
    {
        throw std::runtime_error("must be the same size " __FILE__ "@" LINE_STRING);
    }
    return ip;
}

template <typename T>
DataContainer<T> &DataContainer<T>::operator=(const T Y)
{
    for (size_t idx = 0; idx != this->sz; idx++)
    {
        (*this)[idx] = Y;
    }
    return *this;
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator=(const DataContainer<T> &other)
{
    // Guard self assignment
    if (this == &other)
        return *this;

    this->p_data->clear();
    this->p_data->reserve(other.sz);
    this->sz = other.sz;

    for (size_t idx = 0; idx != this->sz; idx++)
    {
        T val = other[idx];
        (*this)[idx] = val;
    }

    return *this;
};

template <typename T>
const T &DataContainer<T>::operator[](const uint32_t idx) const
{
    return (this->p_data->data()[idx]);
}

template <typename T>
T &DataContainer<T>::operator[](const uint32_t idx)
{
    return (this->p_data->data()[idx]);
}

template <typename T>
DataContainer<T> DataContainer<T>::operator+(const T &Y)
{
    return this->add(Y);
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator+=(const T &Y)
{
    *this = this->add(Y);
    return *this;
};

template <typename T>
DataContainer<T> DataContainer<T>::operator+(const DataContainer<T> &Y)
{
    return this->add(Y);
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator+=(const DataContainer<T> &Y)
{
    *this = this->add(Y);
    return *this;
};

template <typename T>
DataContainer<T> DataContainer<T>::operator-(const T &Y)
{
    return this->sub(Y);
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator-=(const T &Y)
{
    *this = this->sub(Y);
    return *this;
};

template <typename T>
DataContainer<T> DataContainer<T>::operator-(const DataContainer<T> &Y)
{
    return this->sub(Y);
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator-=(const DataContainer<T> &Y)
{
    *this = this->sub(Y);
    return *this;
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator*=(const T &Y)
{
    *this = this->mul(Y);
    return *this;
}

template <typename T>
DataContainer<T> DataContainer<T>::operator*(const T &Y)
{
    return this->mul(Y);
}

template <typename T>
DataContainer<T> &DataContainer<T>::operator*=(const DataContainer<T> &Y)
{
    *this = this->mul(Y);
    return *this;
}

template <typename T>
DataContainer<T> DataContainer<T>::operator*(const DataContainer<T> &Y)
{
    return this->mul(Y);
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator/=(const T &Y)
{
    *this = this->div(Y);
    return *this;
};

template <typename T>
DataContainer<T> DataContainer<T>::operator/(const T &Y)
{
    return this->div(Y);
};

template <typename T>
DataContainer<T> &DataContainer<T>::operator/=(const DataContainer<T> &Y)
{
    *this = this->div(Y);
    return *this;
};

template <typename T>
DataContainer<T> DataContainer<T>::operator/(const DataContainer<T> &Y)
{
    return this->div(Y);
};

template <typename T>
std::string DataContainer<T>::__repr__()
{
    std::stringstream s;

    for (size_t idx = 0; idx != sz; idx++)
    {
        s << (*p_data)[idx] << ',';
        if (idx % 16 == 15)
        {
            s << std::endl;
        }
    }
    s << std::endl;
    return s.str();
}

#endif