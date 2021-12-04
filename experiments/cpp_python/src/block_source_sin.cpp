#include "block_source_sin.h"
#include <iostream>
#include <math.h>
#include <iomanip>
#include "connector_input.h"
#include "connector_output.h"

BlockSource_Sin::BlockSource_Sin(std::string name, float freq, float phase, float amplitude) : BlockInternal::BlockInternal(name, "BlockSource_Sin", 0),
                                                                                               m_freq(freq),
                                                                                               m_phase(phase),
                                                                                               m_amplitude(amplitude)
{
    this->add_input_connector("amplitude");
    this->add_input_connector("frequency");
    this->add_input_connector("phase");
    this->add_output_connector("data");
}

BlockSource_Sin::~BlockSource_Sin()
{
}

RunResult BlockSource_Sin::pre_run(ModelState *ms)
{
#ifdef DEBUG_MESSAGES
    std::cout << "Fnct:" << __PRETTY_FUNCTION__ << " class_id: " << this->class_id << " name: " << this->name << std::endl;
#endif
    (void)ms;
    return RunResult();
}

RunResult BlockSource_Sin::run(ModelState *ms)
{
    float data = m_amplitude * sin((2.0 * M_PI * m_freq * ms->time) + m_phase);
    if (this->debug)
    {
        std::cout << "Fnct:"
                  << __PRETTY_FUNCTION__
                  << " class_id: "
                  << this->class_id
                  << " name: "
                  << this->name
                  << " Data="
                  << std::fixed << std::setprecision(3) << data
                  << std::endl;
    }
    return RunResult(true, false);
}

RunResult BlockSource_Sin::post_run(ModelState *ms)
{
#ifdef DEBUG_MESSAGES
    std::cout << "Fnct:" << __PRETTY_FUNCTION__ << " class_id: " << this->class_id << " name: " << this->name << std::endl;
#endif
    (void)ms;

    return RunResult();
}
