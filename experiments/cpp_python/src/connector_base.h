#ifndef __CONNECTOR_BASE_H__
#define __CONNECTOR_BASE_H__

#include "stdint.h"
#include <string>
class Block;

class ConnectorBase
{
    public:
    ConnectorBase(Block *owner,std::string name):
    m_owner(owner),
    m_name(name){};

    
    Block * m_owner;
    std::string m_name;

};






#endif