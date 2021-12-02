#ifndef __SIMPLE_BLOCK_H__
#define __SIMPLE_BLOCK_H__

#include <iostream>
#include "block.h"
#include "run_result.h"
#include "model_state.h"



class SimpleBlock:public Block
{
public:
    SimpleBlock(std::string name);
    virtual ~SimpleBlock() {}
    virtual RunResult pre_run(ModelState *ms);
    virtual RunResult run(ModelState *ms);
    virtual RunResult post_run(ModelState *ms);

};

#endif