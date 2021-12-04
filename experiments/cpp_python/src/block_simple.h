#ifndef __BLOCK_SIMPLE_H__
#define __BLOCK_SIMPLE_H__

#include <iostream>
#include "block_internal.h"
#include "run_result.h"
#include "model_state.h"

class InputConnector;
class OutputConnector;


class BlockSimple:public BlockInternal
{
public:
    BlockSimple(std::string name);
    virtual ~BlockSimple();
    virtual RunResult pre_run(ModelState *ms);
    virtual RunResult run(ModelState *ms);
    virtual RunResult post_run(ModelState *ms);


};

#endif