#ifndef POC_HPP
#define POC_HPP

#include <cstddef>
#include <functional>
#include <string>
#include <unordered_map>
#include <vector>

namespace poc {

/**
 * @brief Generic handler plugin definition.
 * @param bytes raw bytes of a "command" (which needs de-serialization in the
 * plugin) which will be used/consumed by the plugin.
 * @return serialized bytes of the response.
 */
using plugin_fn_t =
  std::function<std::vector<std::byte>(const std::vector<std::byte>& bytes)>;

/**
 * A mapping between a string to it's corresponding plugin.
 */
using plugins_mapping_t = std::unordered_map<std::size_t, plugin_fn_t>;

/**
 * @brief Load mapping of pythonic entry-points, of the given group name, into
 *        a mapping of strings to plugins.
 * @param group_name the group name of the entry-points, for instance it could
 *                   be "poc.plugins".
 * @return a plugins mapping.
 */
plugins_mapping_t
load_plugins(const std::string& group_name);

}; /* namespace poc */

#endif /* POC_HPP */
