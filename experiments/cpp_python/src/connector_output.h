#ifndef __CONNECTOR_OUTPUT_H__
#define __CONNECTOR_OUTPUT_H__

#include "stdint.h"
#include <string>
#include <list>
#include "connector_base.h"

class OutputConnector:public ConnectorBase
{
    public:
    OutputConnector(Block *owner,const std::string name);
    virtual ~OutputConnector();
    virtual direction_t direction(){return direction_t::OUTPUT;};
    virtual bool connect(ConnectorBase*);

    void register_load(ConnectorBase* p){registered_loads_list.push_back(p);};


    private:
    std::list<ConnectorBase*> registered_loads_list;
};

#endif
