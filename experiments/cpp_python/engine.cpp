#include "engine.h"
#include <iostream>
#include <chrono>
using namespace std::chrono;

Engine::Engine()
{
}

Engine::~Engine()
{
}

bool Engine::register_block(Block *blk)
{
    this->registered_blocks_list.push_back(blk);
    return true;
}

void Engine::run(uint32_t iterations, bool debug)
{
    RunResult r;
    float_t time = (float_t)0.000;
    float_t tick = (float_t)0.001;
    ModelState ms = ModelState(time, tick);
    uint32_t i;
    auto start = high_resolution_clock::now();

    for (i = 0; i < iterations; i++)
    {
        ms = ModelState(time, tick);

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

            if (debug)
            {
                std::cout << "PRE-RUN :" << blk->name << ":" << r.__repr__() << std::endl;
            }
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

            r = blk->run(&ms);
            if (debug)
            {
                std::cout << "RUN :" << blk->name << ":" << r.__repr__() << std::endl;
            }
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

            if (debug)
            {
                std::cout << "POST-RUN :" << blk->name << ":" << r.__repr__() << std::endl;
            }
        }

        time += tick;
    }
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<nanoseconds>(stop - start);
    std::cout << "Engine ran " << i << " iterations in " << duration.count() / 1000 << " uS [ " << duration.count() / i << " nS/iteration ]" << std::endl;
}