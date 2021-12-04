#ifndef __BLOCK_INTERNAL_H__
#define __BLOCK_INTERNAL_H__

#include "block.h"


class BlockInternal:public Block
{
public:
   using Block::Block;
   ~ BlockInternal();
};

#endif