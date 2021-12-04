#ifndef __SSC_EXCEPTION_H__
#define __SSC_EXCEPTION_H__

#include <sstream>
#include <stdexcept>
#include <string>

class ssc_exception_base : public std::runtime_error
{

public:
    ssc_exception_base(const std::string &arg, const char *file, int line) : std::runtime_error(arg)
    {
        std::stringstream s;
        s << file << ":" << line << ": " << arg;
        msg = s.str();
    }
    ~ssc_exception_base() throw() {}
    const char *what() const throw()
    {
        return msg.c_str();
    }

private:
    std::string msg;
};

#define throw_ssc(arg) throw ssc_exception_base(arg, __FILE__, __LINE__);

#endif