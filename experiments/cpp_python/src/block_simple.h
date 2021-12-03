#ifndef __BLOCK_SIMPLE_H__
#define __BLOCK_SIMPLE_H__

#include <iostream>
#include "block.h"
#include "run_result.h"
#include "model_state.h"



class BlockSimple:public Block
{
public:
    BlockSimple(std::string name);
    virtual ~BlockSimple() {}
    virtual RunResult pre_run(ModelState *ms);
    virtual RunResult run(ModelState *ms);
    virtual RunResult post_run(ModelState *ms);

};

#endif