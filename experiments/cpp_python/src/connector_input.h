#ifndef __CONNECTOR_INPUT_H__
#define __CONNECTOR_INPUT_H__

#include "stdint.h"
#include <string>
#include "connector_base.h"

class Block;

class InputConnector : public ConnectorBase
{
public:
    InputConnector(Block *owner,const std::string name) : ConnectorBase(owner, name){};

private:
    ConnectorBase *source;
};

#endif
