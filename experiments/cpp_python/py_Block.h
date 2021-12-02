#ifndef __PY_BLOCK_H__
#define __PY_BLOCK_H__

#include <pybind11/pybind11.h>
#include "block.h"

namespace py = pybind11;

class PyBlock : public Block
{
public:
    using Block::Block;
  
    RunResult pre_run(ModelState*ms) override
    {
        PYBIND11_OVERRIDE_PURE(RunResult, Block, pre_run,ms);
    }

    RunResult run(ModelState*ms) override
    {
        PYBIND11_OVERRIDE_PURE(RunResult, Block, run,ms);
    }

    RunResult post_run(ModelState*ms) override
    {
        PYBIND11_OVERRIDE_PURE(RunResult, Block, post_run,ms);
    }
    
};


#endif