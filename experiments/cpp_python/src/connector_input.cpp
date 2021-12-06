#include "ssc_exceptions.h"
#include "connector_input.h"
#include "connector_output.h"
#include "block.h"
#include <sstream>

InputConnector::InputConnector(Block *owner, const std::string name) : ConnectorBase(owner, name),
                                                                       source(nullptr)
{
}

InputConnector::~InputConnector()
{
    
}

bool InputConnector::connect(ConnectorBase *p_base_connector)
{
    OutputConnector *p_connector = static_cast<OutputConnector *>(p_base_connector);

    if (p_connector == nullptr)
    {
        throw_ssc("NULL Pointer");
    }
    else if (p_connector->direction() != direction_t::OUTPUT)
    {
        std::stringstream s;
        s << "\"" << p_connector->m_name << "\""
          << " of \"" << this->m_owner->name << "\""
          << " is not an output connector";
        throw_ssc(s.str());
    }
    else if (this->source != nullptr)
    {
        std::stringstream s;
        s << "Connector \"" << this->m_name << "\""
          << " of \"" << this->m_owner->name << "\""
          << " is all ready connected";
        throw_ssc(s.str());
    }
    else
    {
        this->source = p_connector;
        p_connector->register_load(this);
    }
    return true;
}

std::string InputConnector::as_string()
{
    return "InputConnector";
}