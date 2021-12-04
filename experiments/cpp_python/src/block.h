#ifndef __BLOCK_H__
#define __BLOCK_H__

#include <iostream>
#include <list>
#include "run_result.h"
#include "model_state.h"

//use forward declaration, instead of including headers to avoid nasty recursive behavior
class ConnectorBase;
class InputConnector;
class OutputConnector;



class Block
{
public:
    Block(std::string name, std::string class_id, uint32_t n_inputs);
    
    //virtual
    virtual ~Block();
    virtual RunResult pre_run(ModelState *ms);
    virtual RunResult run(ModelState *ms);
    virtual RunResult post_run(ModelState *ms);

    

    //common public
    InputConnector *add_input_connector(std::string name);
    OutputConnector *add_output_connector(std::string name);

    InputConnector *get_input_connector_byname(std::string name);
    OutputConnector *get_output_connector_byname(std::string name);

    const std::string get_name(){return this->name;};


    //public members
    std::string name;
    std::string class_id;
    uint32_t max_inputs;    
    
    //debug info
    void enable_debug() { debug = true; };
    std::string get_info();


protected:
    bool debug;

private:
    static uint32_t blk_count;
    std::list<ConnectorBase *> inputConnector_list;
    std::list<ConnectorBase *> outputConnector_list;
    ConnectorBase *get_connector_byname(std::list<ConnectorBase *> &list, std::string name);
};

#endif