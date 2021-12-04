#include "connector_base.h"

ConnectorBase::ConnectorBase(Block *owner, const std::string name) : m_owner(owner),
                                                                     m_name(name)
{
    this->p_dataContainer = nullptr;
}


ConnectorBase::~ConnectorBase()
{

}