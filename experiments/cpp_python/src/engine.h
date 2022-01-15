#ifndef __ENGINE_H__
#define __ENGINE_H__

#include <list>
#include "block.h"
#include "stdint.h"
#include "logger.h"


class Engine
{
public:
    Engine();
    Engine(Logger& logger);
    ~Engine();

    bool register_block(Block *);
    void run(uint32_t iterations,float tick=0);

    void setTickTime(float v)
    {
        tick_time = v;
    }

    float getTickTime()
    {
        return tick_time;
    }

private:
    std::list<Block *> registered_blocks_list;
    float tick_time;
    Logger* logger_inst;
};

#endif