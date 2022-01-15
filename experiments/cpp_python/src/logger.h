#ifndef __LOGGER_H__
#define __LOGGER_H__

#include <string>

#define LOG(LEVEL, LOGGER, FMT, ...)                               \
                                                                   \
    if ((LOGGER != nullptr) && (LEVEL <= LOGGER->get_log_level())) \
    {                                                              \
        LOGGER->log(LEVEL, (char *)FMT, __VA_ARGS__);              \
    }

#define LOG_DEBUG(LOGGER, FMT, ...)                                             \
    if ((LOGGER != nullptr) && (ERROR_LEVEL::DEBUG <= LOGGER->get_log_level())) \
    {                                                                           \
        LOGGER->log(ERROR_LEVEL::DEBUG, (char *)FMT, __VA_ARGS__);              \
    }

#define LOG_INFO(LOGGER, FMT, ...)                                             \
    if ((LOGGER != nullptr) && (ERROR_LEVEL::INFO <= LOGGER->get_log_level())) \
    {                                                                          \
        LOGGER->log(ERROR_LEVEL::INFO, (char *)FMT, __VA_ARGS__);              \
    }

#define LOG_WARN(LOGGER, FMT, ...)                                             \
    if ((LOGGER != nullptr) && (ERROR_LEVEL::WARN <= LOGGER->get_log_level())) \
    {                                                                          \
        LOGGER->log(ERROR_LEVEL::WARN, (char *)FMT, __VA_ARGS__);              \
    }

#define LOG_ERROR(LOGGER, FMT, ...)                                              \
    if ((LOGGER != nullptr) && (ERROR_LEVEL::ERROR <= LOGGER->get_log_level())) \
    {                                                                           \
        LOGGER->log(ERROR_LEVEL::ERROR, (char *)FMT, __VA_ARGS__);              \
    }

enum ERROR_LEVEL
{
    ERROR = 0,
    WARN,
    INFO,
    DEBUG,

};

class Logger
{
public:
    static Logger *get_logger();
    void set_log_level(ERROR_LEVEL l) { this->log_level = l; };
    ERROR_LEVEL get_log_level() { return this->log_level; };

    void log(ERROR_LEVEL l, char *, ...);

private:
    Logger();
    static Logger *inst;
    ERROR_LEVEL log_level;
    std::string level_as_string(ERROR_LEVEL l);
    void __log(ERROR_LEVEL l, char *fmt, va_list args);
};

#endif
