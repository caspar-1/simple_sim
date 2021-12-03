#include "block.h"
#include <sstream>
#include <iostream>

uint32_t Block::blk_count = 0;

Block::Block(std::string name, std::string class_id, uint32_t n_inputs)
{
    std::stringstream s;
    s << name << "_" << blk_count;
    this->name = s.str();
    this->class_id = class_id;
    this->max_inputs = n_inputs;
    Block::blk_count++;
    std::cout << "Fnct:" << __PRETTY_FUNCTION__ << " class_id: " << this->class_id << " name: " << this->name << std::endl;
}

ConnectorBase *Block::get_connector_byname(std::list<ConnectorBase *> &list, std::string name)
{
    ConnectorBase *found = nullptr;
    for (ConnectorBase *c : list)
    {
        if (c->m_name == name)
        {
            found = c;
        }
    }
    return found;
}

ConnectorBase *Block::get_input_connector_byname(std::string name)
{
    return get_connector_byname(this->inputConnector_list, name);
}

ConnectorBase *Block::get_output_connector_byname(std::string name)
{
    return get_connector_byname(this->outputConnector_list, name);
}

ConnectorBase* Block::add_input_connector(std::string name,float default_value)
{
    InputConnector *p = nullptr;
    ConnectorBase* existing=get_input_connector_byname(name);
    if ( existing == nullptr)
    {
        p = new InputConnector(this, name);
        inputConnector_list.push_back(p);
    }
    std::cout << "Block::add_input_connector"<<" : \""<<name<<"\" : "<<(p==nullptr? "FAILED":"OK")<<std::endl;
    return p;
}

ConnectorBase* Block::add_output_connector(std::string name)
{
    OutputConnector *p=nullptr;
    ConnectorBase* existing=get_output_connector_byname(name);
    if ( existing == nullptr)
    {
        p = new OutputConnector(this, name);
        outputConnector_list.push_back(p);
    }
    std::cout << "Block::add_output_connector"<<" : \""<<name<<"\" : "<<(p==nullptr? "FAILED":"OK")<<std::endl;
    return p;
}