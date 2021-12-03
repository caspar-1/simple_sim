#ifndef __BLOCK_H__
#define __BLOCK_H__

#include <iostream>
#include "run_result.h"
#include "model_state.h"
#include "connector_input.h"
#include "connector_output.h"
#include <list>

class Block
{
public:
    Block(std::string name, std::string class_id, uint32_t n_inputs);
    virtual ~Block() {}
    virtual RunResult pre_run(ModelState *ms) = 0;
    virtual RunResult run(ModelState *ms) = 0;
    virtual RunResult post_run(ModelState *ms) = 0;

    ConnectorBase* add_input_connector(std::string name);
    ConnectorBase* add_output_connector(std::string name);

    ConnectorBase *get_input_connector_byname(std::string name);
    ConnectorBase *get_output_connector_byname(std::string name);

    std::string name;
    std::string class_id;
    uint32_t max_inputs;

private:
    static uint32_t blk_count;
    std::list<ConnectorBase *> inputConnector_list;
    std::list<ConnectorBase *> outputConnector_list;
    ConnectorBase *get_connector_byname(std::list<ConnectorBase *> &list, std::string name);
};

#endif