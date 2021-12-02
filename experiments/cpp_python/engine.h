#ifndef __ENGINE_H__
#define __ENGINE_H__


#include <list>
#include "block.h"
#include "stdint.h"

class Engine
{
public:
    Engine();
    ~Engine();

    bool register_block(Block*);
    void run(uint32_t iterations,bool debug=false);

private:
    std::list<Block*> registered_blocks_list;


};

#endif