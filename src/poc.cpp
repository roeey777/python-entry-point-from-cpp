#include <poc/poc.hpp>

extern "C" {
#include <Python.h>  // for Py_IsInitialized.
}

#include <pybind11/embed.h>  // everything needed for embedding
#include <spdlog/spdlog.h>

namespace poc {

namespace py = pybind11;

plugins_mapping_t load_plugins(const std::string& group_name)
{
	plugins_mapping_t mapping;

	if (!Py_IsInitialized()) {
            throw std::runtime_error("Python interpreter is not initialized. Please create a py::scoped_interpreter.");
        }

	spdlog::info("loading plugins for group {}", group_name);

	py::module metadata = py::module::import("importlib.metadata");
	/* entry_points will be of type importlib.metadata.EntryPoints */
	py::object entry_points = metadata.attr("entry_points")();

	py::object group_entries = entry_points.attr("select")(py::arg("group")=group_name);

	for (const auto& entry_point : group_entries) {
            std::string name = entry_point.attr("name").cast<std::string>();
            py::object py_callable = entry_point.attr("load")();

            if (!py::isinstance<py::function>(py_callable)) {
                throw std::runtime_error("Entry point '" + name + "' is not callable");
            }

            plugin_fn_t fn = [py_callable](const std::vector<std::byte>& input_bytes) -> std::vector<std::byte> {
                py::gil_scoped_acquire acquire;  // ensure GIL is held

                // Convert input to py::bytes
                const char* raw_input = reinterpret_cast<const char*>(input_bytes.data());
                py::bytes py_input(raw_input, input_bytes.size());

                // Call the function
                py::object result = py_callable(py_input);

                // Convert result back to bytes
                py::bytes py_output = py::reinterpret_borrow<py::bytes>(result);
                std::string output_str = py_output;

                // Convert to vector<std::byte>
                std::vector<std::byte> output_bytes(output_str.size());
                std::memcpy(output_bytes.data(), output_str.data(), output_str.size());
                return output_bytes;
            };

            mapping.emplace(std::move(name), std::move(fn));
        }

	return mapping;
}

};  /* namespace poc */
