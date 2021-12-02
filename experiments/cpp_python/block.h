#ifndef __BLOCK_H__
#define __BLOCK_H__

#include <iostream>
#include "run_result.h"
#include "model_state.h"


class Block
{
public:
    Block(std::string name, std::string class_id,uint32_t n_inputs);
    virtual ~Block() {}
    virtual RunResult pre_run(ModelState *ms)=0;
    virtual RunResult run(ModelState *ms)=0;
    virtual RunResult post_run(ModelState *ms)=0;


    std::string name;
    std::string class_id;
    uint32_t max_inputs;

private:
    static uint32_t blk_count;
};

#endif