#ifndef __CONNECTOR_OUTPUT_H__
#define __CONNECTOR_OUTPUT_H__

#include "stdint.h"
#include <string>
#include "connector_base.h"



class Block;


class OutputConnector:public ConnectorBase
{
    public:
    OutputConnector(Block *owner,std::string name):ConnectorBase(owner,name){};

};




#endif
