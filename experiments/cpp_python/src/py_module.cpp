#include <pybind11/pybind11.h>
#include <iostream>
#include "block_python_extensible.h"
#include "logger.h"
#include "run_result.h"
#include "engine.h"
#include "block_simple.h"
#include "connector_base.h"
#include "connector_input.h"
#include "connector_output.h"
#include "data_container.h"
#include "block_source_sin.h"


/*
https://pybind11.readthedocs.io/en/stable/index.html
*/


namespace py = pybind11;

std::string version() { return "0.0.0"; }
std::string build_date() { return "<" __DATE__ "@" __TIME__ ">"; }

template <typename T>
void declare_dataContainer(py::module &m, const std::string &typestr)
{
    using Class = DataContainer<T>;
    std::string pyclass_name = std::string("DataContainer_") + typestr;
    py::class_<Class>(m, pyclass_name.c_str())
        .def(py::init<>())
        .def(py::init<size_t>())
        .def(py::init<DataContainer<T>>())
        .def(py::init<std::initializer_list<T>>())
        .def("clear", &DataContainer<T>::clear)
        .def("zero", &DataContainer<T>::zero)
        .def("data_is_ready", &DataContainer<T>::data_is_ready)
        .def("type", &DataContainer<T>::type)
        .def("sum", &DataContainer<T>::sum)
        .def("dot", &DataContainer<T>::dot)
        .def("slice", &DataContainer<T>::slice)

        .def("fill_random", &DataContainer<T>::fill_random)
        .def(
            "__add__", [](DataContainer<T> &self, DataContainer<T> const &other)
            { return self.add(other); },
            py::is_operator())

        .def(
            "__add__", [](DataContainer<T> &self, const T &other)
            { return self.add(other); },
            py::is_operator())

        .def(
            "__sub__", [](DataContainer<T> &self, DataContainer<T> const &other)
            { return self.sub(other); },
            py::is_operator())

        .def(
            "__sub__", [](DataContainer<T> &self, const T &other)
            { return self.sub(other); },
            py::is_operator())

        .def(
            "__mul__", [](DataContainer<T> &self, DataContainer<T> const &other)
            { return self.mul(other); },
            py::is_operator())

        .def(
            "__mul__", [](DataContainer<T> &self, const T &other)
            { return self.mul(other); },
            py::is_operator())

        .def(
            "__truediv__", [](DataContainer<T> &self, DataContainer<T> const &other)
            { return self.div(other); },
            py::is_operator())

        .def(
            "__truediv__", [](DataContainer<T> &self, const T &other)
            { return self.div(other); },
            py::is_operator())

        .def(
            "push", [](DataContainer<T> &self, T data)
            { return self.push(data); })

        .def(
            "pop", [](DataContainer<T> &self)
            {
                bool is_ok = false;
                T data;
                data = self.pop(is_ok);
                return std::make_tuple(data, is_ok); })

        .def(
            "init", [](DataContainer<T> &self, py::list data_list)
            {
                self.p_data->clear();
                for (auto item : data_list)
                {
                    self.p_data->push_back(item.cast<T>());
                }
                self.update_size(); })

        .def_property("size", &DataContainer<T>::get_size, nullptr)

        .def("__repr__", &DataContainer<T>::__repr__);
}

PYBIND11_MODULE(simpleSimCore, m)
{
    m.def("version", &version, "get module version");
    m.def("build_date", &build_date, "get build date");

    py::enum_<ERROR_LEVEL>(m, "ERROR_LEVEL")
        .value("ERROR", ERROR)
        .value("WARN", WARN)
        .value("INFO", INFO)
        .value("DEBUG", DEBUG)
        .export_values();

    py::class_<Logger>(m, "Logger")
        .def_static("get_logger", &Logger::get_logger)
        .def_property("log_level", &Logger::get_log_level, &Logger::set_log_level);

    py::class_<Engine>(m, "Engine")
        .def(py::init<>())
        .def(py::init<Logger &>())
        .def("register_block", &Engine::register_block)
        .def("run", &Engine::run);

    py::class_<RunResult>(m, "RunResult")
        .def(py::init<>())
        .def_readwrite("has_run", &RunResult::has_run)
        .def_readwrite("update_display", &RunResult::update_display)
        .def_readwrite("message", &RunResult::message);

    py::class_<ModelState>(m, "ModelState")
        .def(py::init<float_t, float_t>())
        .def_readonly("time", &ModelState::time)
        .def_readonly("d_time", &ModelState::d_time);

    py::enum_<direction_t>(m, "Direction")
        .value("INPUT", direction_t::INPUT)
        .value("OUTPUT", direction_t::OUTPUT);

    py::class_<ConnectorBase>(m, "ConnectorBase")
        .def("direction", &ConnectorBase::direction)
        .def("connect", &ConnectorBase::connect)
        .def("__repr__", &ConnectorBase::as_string)
        .def_readonly("name", &ConnectorBase::m_name)
        .def_readonly("owner", &ConnectorBase::m_owner);

    py::class_<InputConnector, ConnectorBase>(m, "InputConnector");

    py::class_<OutputConnector, ConnectorBase>(m, "OutputConnector");

    py::class_<Block>(m, "Block")
        .def("enable_debug", &Block::enable_debug, "enable simple debug")
        .def("get_input_connector_byname", &Block::get_input_connector_byname)
        .def("get_output_connector_byname", &Block::get_output_connector_byname)
        .def("__repr__", &Block::as_string)
        .def_readonly("name", &Block::name)
        .def_readonly("class_id", &Block::class_id);

    py::class_<Block, BlockPythonExtensible>(m, "pyBlock", py::module_local())
        .def(py::init<const std::string &, const std::string &, uint32_t>())
        .def("pre_run", &Block::pre_run)
        .def("run", &Block::run)
        .def("post_run", &Block::post_run)
        .def("add_input_connector", &Block::add_input_connector)
        .def("add_output_connector", &Block::add_output_connector)
        .def("get_input_connector_byname", &Block::get_input_connector_byname)
        .def("get_output_connector_byname", &Block::get_output_connector_byname)
        .def("enable_debug", &Block::enable_debug)
        .def_readonly("name", &Block::name)
        .def_readonly("class_id", &Block::class_id);

    py::class_<BlockInternal, Block>(m, "BlockInternal");

    py::class_<BlockSimple, BlockInternal>(m, "BlockSimple")
        .def(py::init<std::string>())
        .def("__repr__", &Block::as_string);

    py::class_<BlockSource_Sin, BlockInternal>(m, "BlockSource_Sin")
        .def(py::init<std::string, float, float, float>())
        .def("__repr__", &Block::as_string);

    declare_dataContainer<float>(m, "float");
    declare_dataContainer<std::complex<float>>(m, "complex");
    declare_dataContainer<int>(m, "int");
}