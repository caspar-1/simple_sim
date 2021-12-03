#include "block.h"
#include <sstream>

uint32_t Block::blk_count = 0;

Block::Block(std::string name, std::string class_id, uint32_t n_inputs)
{
    
    std::stringstream s;
    s << name << "_" << blk_count;
    this->name = s.str();
    this->class_id = class_id;
    this->max_inputs = n_inputs;
    Block::blk_count++;
    std::cout<< "Fnct:"<< __PRETTY_FUNCTION__ <<" class_id: "<<this->class_id<<" name: "<<this->name<<std::endl;
}
