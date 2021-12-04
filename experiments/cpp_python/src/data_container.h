#ifndef __DATA_CONTAINER_H__
#define __DATA_CONTAINER_H__

#include <iostream>
#include "data_object_base.h"



class DataContainer
{
public:
    DataContainer();
    ~DataContainer();
    bool data_is_ready();
    DataObjectBase* get_data();
    void set_data(DataObjectBase*);





private:
    DataObjectBase* p_data;
    bool is_valid;
};

#endif