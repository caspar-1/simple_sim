#include <sstream>
#include <iostream>
#include "block_internal.h"
#include "connector_input.h"
#include "connector_output.h"

BlockInternal::~BlockInternal()
{
#ifdef DEBUG_MESSAGES
    std::cout << "BlockInternal destructor : " << this->name << std::endl;

    std::cout << "deleting input connector:" << std::endl;
    for (ConnectorBase *p : this->inputConnector_list)
    {
        std::cout << "  -" << p->m_name << std::endl;
        delete p;
    }
    this->inputConnector_list.clear();
    std::cout << "deleting output connector:" << std::endl;
    for (ConnectorBase *p : this->outputConnector_list)
    {
        std::cout << "  -" << p->m_name << std::endl;
        delete p;
    }
    this->outputConnector_list.clear();
#endif
}