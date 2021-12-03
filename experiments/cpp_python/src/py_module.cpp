#include <pybind11/pybind11.h>
#include <iostream>
#include "block_python_extensible.h"
#include "run_result.h"
#include "engine.h"
#include "block_simple.h"
#include "connector_base.h"
#include "connector_input.h"
#include "connector_output.h"

#include "block_source_sin.h"

/*
https://pybind11.readthedocs.io/en/stable/index.html
*/

namespace py = pybind11;

std::string version() { return "0.0.0"; }
std::string build_date() { return "<" __DATE__ "@" __TIME__ ">"; }

PYBIND11_MODULE(simpleSimCore, m)
{
    m.def("version", &version, "get module version");
    m.def("build_date", &build_date, "get build date");

    py::class_<Engine>(m, "Engine")
        .def(py::init<>())
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

    py::class_<ConnectorBase>(m, "ConnectorBase")
        .def(py::init< Block *, std::string >)
        .def_readonly("name", &InputConnector::m_name)
        .def_readonly("owner", &InputConnector::m_owner);

    py::class_<InputConnector, ConnectorBase>(m, "InputConnector")
        .def(py::init< Block *, std::string>)
        .def_readonly("name", &InputConnector::m_name)
        .def_readonly("owner", &InputConnector::m_owner);

    py::class_<OutputConnector, ConnectorBase>(m, "OutputConnector")
        .def(py::init< Block *, std::string>())
        .def_readonly("name", &OutputConnector::m_name)
        .def_readonly("owner", &OutputConnector::m_owner);

    py::class_<Block>(m, "abstract__Block")
        .def_readonly("name", &Block::name)
        .def_readonly("class_id", &Block::class_id);

    py::class_<Block, BlockPythonExtensible>(m, "Block", py::module_local())
        .def(py::init<const std::string &, const std::string &, uint32_t>())
        .def("pre_run", &Block::pre_run)
        .def("run", &Block::run)
        .def("post_run", &Block::post_run)
        .def("add_input_connector", &Block::add_input_connector)
        .def("add_output_connector", &Block::add_output_connector)
        .def_readonly("name", &Block::name)
        .def_readonly("class_id", &Block::class_id);

    py::class_<BlockSimple, Block>(m, "BlockSimple")
        .def(py::init<std::string>())
        .def_readonly("name", &BlockSimple::name)
        .def_readonly("class_id", &BlockSimple::class_id);

    py::class_<BlockSource_Sin, Block>(m, "BlockSource_Sin")
        .def(py::init<std::string, float, float, float>())
        .def_readonly("name", &BlockSource_Sin::name)
        .def_readonly("class_id", &BlockSource_Sin::class_id);
}