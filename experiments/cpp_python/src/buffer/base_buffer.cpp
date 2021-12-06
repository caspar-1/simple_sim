#include "base_buffer.h"
#include <iostream>

BaseBuffer::BaseBuffer()
{
    std::cout<<"BaseBuffer contructor"<<std::endl;
    this->sz=0;
    this->idx=0;
}


BaseBuffer::BaseBuffer(uint32_t sz)
{
    std::cout<<"BaseBuffer contructor"<<std::endl;
    this->sz=sz;
    this->idx=0;
}

BaseBuffer::~BaseBuffer()
{
    std::cout<<"BaseBuffer destructor"<<std::endl;

}