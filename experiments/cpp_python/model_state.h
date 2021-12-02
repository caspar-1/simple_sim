#ifndef __MODEL_STATE_H__
#define __MODEL_STATE_H__

#include <sstream>

class ModelState
{
public:
    ModelState(float_t _time,float_t _d_time):time(_time),d_time(_d_time){};
    float_t time;
    float_t d_time;
};

#endif
