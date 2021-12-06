#ifndef __CONNECTOR_BASE_H__
#define __CONNECTOR_BASE_H__

#include "stdint.h"
#include <string>
#include "data_container.h"

typedef enum{
    INPUT=0,
    OUTPUT=1
}direction_t;

class Block;

class ConnectorBase
{
    public:
    ConnectorBase(Block *owner,const std::string name);
    virtual ~ConnectorBase();

    virtual bool connect(ConnectorBase*)=0;
    virtual direction_t direction()=0;
    virtual  std::string as_string()=0;



    Block * m_owner;
    std::string m_name;
    DataContainer *p_dataContainer;

};






#endif