#include "data_container.h"

DataContainer::DataContainer()
{
    this->p_data = nullptr;
}

DataContainer::~DataContainer()
{
}

bool DataContainer::data_is_ready()
{
    return ((this->p_data != nullptr) & (this->is_valid));
}

DataObjectBase *DataContainer::get_data()
{
    DataObjectBase *p = nullptr;
    if (this->is_valid)
    {
        p = this->p_data;
    }
    return p;
}

void DataContainer::set_data(DataObjectBase *_data)
{
    if (_data != nullptr)
    {
        this->is_valid = true;
        this->p_data = _data;
    }
    else
    {
        this->is_valid = false;
    }
}