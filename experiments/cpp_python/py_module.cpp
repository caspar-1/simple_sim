#include <pybind11/pybind11.h>
#include <iostream>
#include "py_Block.h"
#include "run_result.h"
#include "engine.h"
#include "simple_block.h"

/*
https://pybind11.readthedocs.io/en/stable/index.html
*/


namespace py = pybind11;

std::string version(){return "0.0.0";}
std::string build_date(){return "<" __DATE__ "@" __TIME__ ">";}


PYBIND11_MODULE(simpleSimCore, m)
{
    py::class_<RunResult>(m, "RunResult")
        .def(py::init<>())
        .def_readwrite("has_run", &RunResult::has_run)
        .def_readwrite("update_display", &RunResult::update_display)
        .def_readwrite("message", &RunResult::message);

    py::class_<ModelState>(m, "ModelState")
        .def(py::init<float_t,float_t>())
        .def_readonly("time", &ModelState::time)
        .def_readonly("d_time", &ModelState::d_time);

    py::class_<SimpleBlock>(m, "SimpleBlock")
        .def(py::init<const std::string &>())
        .def_readonly("name", &SimpleBlock::name)
        .def_readonly("class_id", &SimpleBlock::class_id);

       
    py::class_<Block, PyBlock>(m, "Block")
        .def(py::init<const std::string &,const std::string &,uint32_t>())
        .def("pre_run", &Block::pre_run)
        .def("run", &Block::run)
        .def("post_run", &Block::post_run)
        .def_readonly("name", &Block::name)
        .def_readonly("class_id", &Block::class_id);

    py::class_<Engine>(m, "Engine")
        .def(py::init<>())
        .def("register_block", &Engine::register_block)
        .def("run", &Engine::run);

    m.def("version", &version,"get module version");
    m.def("build_date", &build_date,"get build date");
}