#ifndef __BUFFER_H__
#define __BUFFER_H__

#include <vector>
#include "stdint.h"
#include "base_buffer.h"
#include <iostream>

template <class T>
class Buffer:public BaseBuffer
{

public:
    Buffer();
    Buffer(uint32_t sz);
    ~Buffer();
    Buffer (const Buffer &obj);

    bool addData(T);
    void clean();

private:
    std::vector<T> storage;
    
};


template<class T>
Buffer<T>::Buffer():BaseBuffer()
{
    std::cout<<"Buffer contructor"<<std::endl;
    storage.reserve(0);
}

template<class T>
Buffer<T>::Buffer(uint32_t sz):BaseBuffer(sz)
{
    std::cout<<"Buffer contructor"<<std::endl;
    storage.reserve(sz);
}

template<class T>
Buffer<T>::~Buffer()
{
    std::cout<<"Buffer destructor"<<std::endl;
}


template<class T>
Buffer<T>::Buffer (const Buffer &obj)
{
    this->sz=obj.sz;
    this->idx=obj.idx;
    this->storage=obj.storage;
}



template<class T> 
bool Buffer<T>::addData(T data)
{
    
    this->storage[idx]=data;
    if(idx!=sz)
    {
        idx++;
    }
    return true;
    
}



template<class T> 
void Buffer<T>::clean()
{
    std::fill(this->storage.begin(), this->storage.end(), (T)0);
}
















#endif