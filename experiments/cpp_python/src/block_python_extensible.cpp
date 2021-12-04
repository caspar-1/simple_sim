
#include <pybind11/pybind11.h>
#include "block_python_extensible.h"

namespace py = pybind11;

BlockPythonExtensible::~BlockPythonExtensible()
{
#ifdef DEBUG_MESSAGES
    std::cout << "destructor<BlockPythonExtensible> : " << this->name << std::endl;
#endif
}