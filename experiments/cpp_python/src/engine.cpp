#include "engine.h"
#include <iostream>
#include <chrono>
#include <cmath>
#include "logger.h"

using namespace std::chrono;

Engine::Engine()
{
    tick_time = (float)0.001;
    this->logger_inst = nullptr;
}

Engine::Engine(Logger &logger_inst)
{
    tick_time = (float)0.001;
    this->logger_inst = &logger_inst;
}

Engine::~Engine()
{
}

bool Engine::register_block(Block *blk)
{
    std::cout << "Fnct:" << __PRETTY_FUNCTION__ << " class_id: " << blk->class_id << " name: " << blk->name << std::endl;
    this->registered_blocks_list.push_back(blk);
    return true;
}

void Engine::run(uint32_t iterations, float tick)
{
    RunResult r;
    float time = (float)0.000;
    if (tick != 0)
    {
        this->tick_time = std::abs(tick);
    }

    ModelState ms = ModelState(time, tick_time);
    uint32_t i;
    auto start = high_resolution_clock::now();

    std::cout << "-------------------------------------------" << std::endl;
    std::cout << "--               ENGINE                  --" << std::endl;
    std::cout << "-------------------------------------------" << std::endl;

    LOG(ERROR_LEVEL::WARN, logger_inst, "LOGGER is Enabled, this will comprimise performance", 0);

    ms = ModelState(0, 0);
    for (i = 0; i < iterations; i++)
    {

        ms.time = time;
        ms.d_time = tick_time;

        for (Block *blk : this->registered_blocks_list)
        {
            try
            {
                r = blk->pre_run(&ms);
            }
            catch (const std::exception &e)
            {
                std::cerr << e.what() << '\n';
            }

            LOG_DEBUG(logger_inst, "%i:ENGINE:PRE-RUN  BLOCK:%s REPORT:%s", i, blk->get_name_cstr(), r.__repr__cstr());
        }

        for (Block *blk : this->registered_blocks_list)
        {
            try
            {
                r = blk->run(&ms);
            }
            catch (const std::exception &e)
            {
                std::cerr << e.what() << '\n';
            }

            LOG_DEBUG( logger_inst, "%d:ENGINE:RUN BLOCK:%s REPORT:%s", i, blk->get_name_cstr(), r.__repr__cstr());
        }

        for (Block *blk : this->registered_blocks_list)
        {
            try
            {
                r = blk->post_run(&ms);
            }
            catch (const std::exception &e)
            {
                std::cerr << e.what() << '\n';
            }

            LOG_DEBUG( logger_inst, "%d:ENGINE:POST-RUN BLOCK:%s REPORT:%s", i, blk->get_name_cstr(), r.__repr__cstr());
        }

        time = time + tick_time;
    }
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<nanoseconds>(stop - start);

    std::cout << "Engine ran " << i << " iterations in " << duration.count() / 1000 << "uS  [" << duration.count() / i << "nS/iteration]";
}