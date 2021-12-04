#ifndef __CONNECTOR_INPUT_H__
#define __CONNECTOR_INPUT_H__

#include "stdint.h"
#include <string>
#include "connector_base.h"



class InputConnector : public ConnectorBase
{
public:
    InputConnector(Block *owner,const std::string name);
    virtual ~InputConnector();
    virtual direction_t direction(){return direction_t::INPUT;};
    virtual bool connect(ConnectorBase*);
    ConnectorBase * get_source(){return source;};
    void set_source(ConnectorBase *p){source=p;};

private:
    ConnectorBase *source;
};

#endif
