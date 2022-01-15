#include "logger.h"
#include <stdarg.h>
#include <memory>
#include <stdexcept>
#include <iostream>
#include <ctime>
#include <iomanip>
#include "helper_string_format.h"


Logger *Logger::inst = nullptr;

Logger::Logger()
{
}

Logger *Logger::get_logger()
{
    if (Logger::inst == nullptr)
    {
        Logger::inst = new Logger();
    }
    return Logger::inst;
}

void Logger::__log(ERROR_LEVEL l, char *fmt, va_list args)
{
    if (l <= log_level)
    {
        auto t = std::time(nullptr);
        auto tm = *std::localtime(&t);
        std::string s = string_format(fmt, args);
        std::cout << std::put_time(&tm, "%d-%m-%Y %H-%M-%S") << " : ";
        std::cout << level_as_string(l) << " : ";
        std::cout << s;
        std::cout << std::endl;
    }
}

void Logger::log(ERROR_LEVEL l, char *fmt, ...)
{
    va_list args;
    va_start(args, fmt);
    __log(l, fmt, args);
    va_end(args);
}



std::string Logger::level_as_string(ERROR_LEVEL l)
{
    std::string s;
    switch (l)
    {
    case ERROR_LEVEL::DEBUG:
    {
        s = "DEBUG";
        break;
    }
    case ERROR_LEVEL::INFO:
    {
        s = "INFO";
        break;
    }
    case ERROR_LEVEL::WARN:
    {
        s = "WARNING";
        break;
    }
    case ERROR_LEVEL::ERROR:
    {
        s = "ERROR";
        break;
    }
    default:
    {
        s = "UNDEFINED";
    }
    }
    return s;
}
