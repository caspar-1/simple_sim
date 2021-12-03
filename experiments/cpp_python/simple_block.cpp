#include "simple_block.h"
#include <iostream>

SimpleBlock::SimpleBlock(std::string name):
Block::Block(name,"SimpleBlock", 0)
{
}


RunResult SimpleBlock::pre_run(ModelState *ms)
{
    //std::cout<< "Fnct:"<< __PRETTY_FUNCTION__ <<" class_id: "<<this->class_id<<" name: "<<this->name<<std::endl;
    (void)ms;
    RunResult rr;
    rr.has_run = false;
    rr.update_display = false;
    rr.message = "pre_run";
    return rr;
}

RunResult SimpleBlock::run(ModelState *ms)
{
    //std::cout<< "Fnct:"<< __PRETTY_FUNCTION__ <<" class_id: "<<this->class_id<<" name: "<<this->name<<std::endl;
    (void)ms;
    RunResult rr;
    rr.has_run = true;
    rr.update_display = true;
    rr.message = "run";
    return rr;
}

RunResult SimpleBlock::post_run(ModelState *ms)
{
    //std::cout<< "Fnct:"<< __PRETTY_FUNCTION__ <<" class_id: "<<this->class_id<<" name: "<<this->name<<std::endl;
    (void)ms;
    RunResult rr;
    rr.has_run = false;
    rr.update_display = false;
    rr.message = "post_run";
    return rr;
}