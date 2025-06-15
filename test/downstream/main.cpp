#include <cstddef>
#include <iostream>
#include <vector>

#include <pybind11/embed.h> // everything needed for embedding

#include <poc/poc.hpp>

#ifndef UNUSED
#define UNUSED(x) ((void)x)
#endif

namespace py = pybind11;

int
main(int argc, char** argv)
{
  UNUSED(argc);
  UNUSED(argv);

  std::string raw_input_to_plugin = "asdf";
  const std::byte* begin =
    reinterpret_cast<const std::byte*>(raw_input_to_plugin.data());
  const std::byte* end = begin + raw_input_to_plugin.size();
  std::vector<std::byte> input_to_plugin(begin, end);

  py::scoped_interpreter guard{}; // Initialize Python interpreter

  poc::plugins_mapping_t mapping = poc::load_plugins("example.group");

  poc::plugin_fn_t plugin = mapping.at("hello");
  (void)plugin(input_to_plugin);

  return 0;
}
