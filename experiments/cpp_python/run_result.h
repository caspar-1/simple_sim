#ifndef __RUN_RESULT_H__
#define __RUN_RESULT_H__

#include <sstream>

class RunResult
{
public:
    RunResult(){};
    bool has_run;
    bool update_display;
    std::string message;

    std::string __repr__() { std::stringstream x;x << has_run << ":" << update_display << ":" << message;return x.str(); };
};

#endif
