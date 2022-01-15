#ifndef __RUN_RESULT_H__
#define __RUN_RESULT_H__

#include <sstream>

class RunResult
{
public:
    RunResult() : has_run(0),
                  update_display(0),
                  message("-"){};

    RunResult(bool has_run, bool update_display) : has_run(has_run),
                                                   update_display(update_display),
                                                   message("-"){};

    RunResult(bool has_run, bool update_display, std::string message) : has_run(has_run),
                                                                        update_display(update_display),
                                                                        message(message){};

    bool has_run;
    bool update_display;
    std::string message;

    std::string __repr__()
    {
        std::stringstream x;
        x << "[ HAS RUN:" << (has_run == true ? "Y" : "N") << " UPDATE DISPLAY:" << (update_display == true ? "Y" : "N") << " MESSAGE:" << message << " ]";
        report_string = x.str();
        return report_string;
    };

    const char *__repr__cstr()
    {
        __repr__();
        return report_string.c_str();
    };

private:
    std::string report_string;
};

#endif
