#ifndef __BLOCK_SOURCE_SIN_H__
#define __BLOCK_SOURCE_SIN_H__

#include <iostream>
#include "block_internal.h"
#include "run_result.h"
#include "model_state.h"

class InputConnector;
class OutputConnector;




class BlockSource_Sin:public BlockInternal
{
public:
    BlockSource_Sin(std::string name,float freq,float phase,float amplitude);
    virtual ~BlockSource_Sin();
    virtual RunResult pre_run(ModelState *ms);
    virtual RunResult run(ModelState *ms);
    virtual RunResult post_run(ModelState *ms);

private:
    float m_freq;
    float m_phase;
    float m_amplitude;
   


};

#endif
