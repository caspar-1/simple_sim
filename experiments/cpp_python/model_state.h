#ifndef __MODEL_STATE_H__
#define __MODEL_STATE_H__

#include <sstream>
#include "stdint.h"

class ModelState
{
public:
    ModelState(float _time,float _d_time):time(_time),d_time(_d_time){};
    float time;
    float d_time;
};

#endif
