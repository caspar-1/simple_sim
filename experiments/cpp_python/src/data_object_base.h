#ifndef __DATA_OBJECT_BASE_H__
#define __DATA_OBJECT_BASE_H__

#include <iostream>

class DataObjectBase
{
public:
    DataObjectBase();
    ~DataObjectBase();

private:
    bool is_valid;
};

#endif