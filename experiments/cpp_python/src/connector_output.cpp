#include "ssc_exceptions.h"
#include "connector_output.h"
#include "connector_input.h"
#include "block.h"
#include <sstream>

OutputConnector::OutputConnector(Block *owner, const std::string name) : ConnectorBase(owner, name)
{
}

OutputConnector::~OutputConnector()
{

}

bool OutputConnector::connect(ConnectorBase *p_base_connector)
{
    InputConnector *p_connector = static_cast<InputConnector *>(p_base_connector);

    if (p_connector == nullptr)
    {
        throw_ssc("NULL Pointer");
    }
    else if (p_connector->direction() != direction_t::INPUT)
    {
        std::stringstream s;
        s << "\"" << p_connector->m_name << "\""
          << " of \"" << this->m_owner->name << "\""
          << " is not an input connector";
        throw_ssc(s.str());
    }
    else if (p_connector->get_source() != nullptr)
    {
        std::stringstream s;
        s << "Connector \"" << p_connector->m_name << "\""
          << " of \"" << this->m_owner->name << "\""
          << " is allready connected";
        throw_ssc(s.str());
    }
    else
    {
        p_connector->set_source(this);
        this->register_load(p_base_connector);
    }
    return true;
}

std::string OutputConnector::as_string()
{
    return "OutputConnector";
}