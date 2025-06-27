cmake_minimum_required(VERSION 3.15)
project(
    downstream
    VERSION 1.0.0
    LANGUAGES CXX)

find_package(Poc 0.1.0 REQUIRED)

add_executable(downstream main.cpp)
target_link_libraries(downstream PRIVATE Poc::Poc)

enable_testing()
add_test(NAME downstream COMMAND downstream)
