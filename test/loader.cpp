#include <cstddef>
#include <iostream>
#include <optional>
#include <string>
#include <vector>

#include <Python.h> // Required for PyErr_Clear
#include <argparse/argparse.hpp>
#include <pybind11/embed.h> // everything needed for embedding

#include <poc/poc.hpp>

#ifndef UNUSED
#define UNUSED(x) ((void)x)
#endif

namespace py = pybind11;

int
main(int argc, char** argv);

/**
 * @brief print all the loaded plugins (entry-points) from the
 *        given entry-points group name.
 * @param group_name the name of the entry-points group to load plugins from.
 * @return 0 on success, 1 otherwise.
 *
 * @note there is name filtering for entry-points prior to loading, so it is
 *       possible that a fully & properly registered entry-point won't be loaded
 *       due to it's name.
 */
static int
list_plugins(const std::string& group_name);

/**
 * @brief execute a given plugin name, from the given group name, with the given
 *        data. print out the result.
 * @param group_name the name of the entry-points group to load plugins from.
 * @param plugin_name the name of the entry-point to execute.
 * @param raw_data the data which will be passed as input to the plugin.
 * @return 0 on success, 1 otherwise.
 *
 * @note there is name filtering for entry-points prior to loading, so it is
 *       possible that a fully & properly registered entry-point won't be loaded
 *       due to it's name.
 */
static int
execute_plugin(const std::string& group_name,
               const std::size_t plugin_name,
               const std::string& raw_data);

int
main(int argc, char** argv)
{
  std::string group_name;
  std::size_t entry_point_name;
  std::string raw_data;

  argparse::ArgumentParser program("test");
  program.add_description(
    "Small utility used to ease integration testing of the library");
  program.add_argument("--no-interpreter-init")
    .help("Don't initialize the python interpreter")
    .flag();

  argparse::ArgumentParser list_command("list");
  list_command.add_description(
    "List the names of all the loaded (after filterring) plugins");
  list_command.add_argument("--group-name")
    .help("The name of the entry-points group to be loaded")
    .required()
    .store_into(group_name);

  argparse::ArgumentParser execute_command("exec");
  execute_command.add_description(
    "Execute a given entry-point by it's name, group & pass input into it");
  execute_command.add_argument("--group-name")
    .help("The name of the entry-points group to be loaded")
    .required()
    .store_into(group_name);
  execute_command.add_argument("--entry-point")
    .help("The name of the entry-point to be invoked")
    .required()
    .scan<'u', std::size_t>()
    .store_into(entry_point_name);
  execute_command.add_argument("raw_data")
    .help("Raw data (bytes) to be passed to the entry-point")
    .store_into(raw_data);

  program.add_subparser(list_command);
  program.add_subparser(execute_command);

  try {
    program.parse_args(argc, argv);
  } catch (const std::exception& err) {
    std::cerr << err.what() << std::endl;
    std::cout << program;
    return 1;
  }

  std::optional<py::scoped_interpreter> guard;

  if (program.get<bool>("--no-interpreter-init") != true) {
    guard.emplace(); /* Initialize Python interpreter */
  }

  int result = -1;
  if (program.is_subcommand_used(list_command)) {
    result = list_plugins(list_command.get<std::string>("--group-name"));
  } else if (program.is_subcommand_used(execute_command)) {
    result = execute_plugin(execute_command.get<std::string>("--group-name"),
                            execute_command.get<std::size_t>("--entry-point"),
                            execute_command.get<std::string>("raw_data"));
  }

  return result;
}

int
list_plugins(const std::string& group_name)
{
  try {
    poc::plugins_mapping_t mapping = poc::load_plugins(group_name);

    if (mapping.empty()) {
      std::cout << "There are no available plugins to load in group "
                << group_name << std::endl;
    } else {
      for (auto const& item : mapping) {
        std::cout << item.first << std::endl;
      }
    }
  } catch (const std::runtime_error& err) {
    std::cerr << err.what() << std::endl;
    return 1;
  }

  return 0;
}

int
execute_plugin(const std::string& group_name,
               const std::size_t plugin_name,
               const std::string& raw_data)
{
  const std::byte* begin = reinterpret_cast<const std::byte*>(raw_data.data());
  const std::byte* end = begin + raw_data.size();
  std::vector<std::byte> input_to_plugin(begin, end);

  try {
    poc::plugins_mapping_t mapping = poc::load_plugins(group_name);

    if (mapping.end() == mapping.find(plugin_name)) {
      std::cerr << "There is no plugin called " << plugin_name << " in group "
                << group_name << std::endl;
      return 1;
    }

    poc::plugin_fn_t plugin = mapping.at(plugin_name);

    try {
      std::vector<std::byte> output = plugin(input_to_plugin);

      for (auto const& e : output) {
        std::cout << static_cast<char>(e);
      }
      std::cout << std::endl;

    } catch (py::error_already_set& e) {
      /* catch all python's exceptions */
      std::cerr << "Caught an exception from python, which is: " << e.what()
                << std::endl;
      PyErr_Clear();
      return 1;
    }
  } catch (const std::runtime_error& err) {
    std::cerr << err.what() << std::endl;
    return 1;
  }

  return 0;
}
