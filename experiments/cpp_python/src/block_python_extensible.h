#ifndef __BLOCK_PYTHON_EXTENSIBLE_H__
#define __BLOCK_PYTHON_EXTENSIBLE_H__

#include <pybind11/pybind11.h>
#include "block.h"
#include <iostream>

namespace py = pybind11;

class BlockPythonExtensible : public Block
{
public:
    using Block::Block;

    ~BlockPythonExtensible();
  
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