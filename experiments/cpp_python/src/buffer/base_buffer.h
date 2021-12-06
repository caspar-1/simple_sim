#ifndef __BASE_BUFFER_H__
#define __BASE_BUFFER_H__

#include "stdint.h"
#include <complex>



class BaseBuffer
{

public:
    BaseBuffer();
    BaseBuffer(uint32_t sz);
    BaseBuffer(const BaseBuffer &obj);
    virtual ~BaseBuffer();

   
    virtual bool addData(float){return false;};
    virtual bool addData(uint32_t){return false;};
    virtual bool addData(std::complex<float>){return false;};
    
    virtual void clean()=0;
 

    virtual bool is_full() { return idx == sz; };
    virtual void reset() { sz = 0; };

protected:
    uint32_t sz;
    uint32_t idx;
};
#endif