#include "block_simple.h"
#include <iostream>
#include "connector_input.h"
#include "connector_output.h"

BlockSimple::BlockSimple(std::string name) : BlockInternal::BlockInternal(name, "BlockSimple", 0)
{
    this->add_input_connector("A");
    this->add_input_connector("B");
    this->add_output_connector("OUT");
}

BlockSimple::~BlockSimple()
{
}

RunResult BlockSimple::pre_run(ModelState *ms)
{

#ifdef DEBUG_MESSAGES
    std::cout << "Fnct:" << __PRETTY_FUNCTION__ << " class_id: " << this->class_id << " name: " << this->name << std::endl;
#endif
    (void)ms;
    RunResult rr;
    rr.has_run = false;
    rr.update_display = false;
    rr.message = "pre_run";
    return rr;
}

RunResult BlockSimple::run(ModelState *ms)
{
#ifdef DEBUG_MESSAGES
    std::cout << "Fnct:" << __PRETTY_FUNCTION__ << " class_id: " << this->class_id << " name: " << this->name << std::endl;
#endif
    (void)ms;
    RunResult rr;
    rr.has_run = true;
    rr.update_display = true;
    rr.message = "run";
    return rr;
}

RunResult BlockSimple::post_run(ModelState *ms)
{
#ifdef DEBUG_MESSAGES
    std::cout << "Fnct:" << __PRETTY_FUNCTION__ << " class_id: " << this->class_id << " name: " << this->name << std::endl;
#endif
    (void)ms;
    RunResult rr;
    rr.has_run = false;
    rr.update_display = false;
    rr.message = "post_run";
    return rr;
}
