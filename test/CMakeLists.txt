cmake_minimum_required(VERSION 3.15)

# argparse is a single-header library, so it only needs to be added
# to the target include directories, no need to link against it
# since there is nothing to be linked against...
find_package(argparse 3.2 REQUIRED)

add_executable(loader loader.cpp)
target_include_directories(loader PRIVATE ${argparse_INCLUDE_DIRS})
target_link_libraries(loader PRIVATE Poc::Poc)

enable_testing()
add_test(NAME loader COMMAND loader)
