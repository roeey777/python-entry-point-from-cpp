cmake_minimum_required(VERSION 3.15)

project(Fact LANGUAGES CXX)

include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

option(ENABLE_TESTING "Enable Test Builds" ON)
option(ENABLE_DOCS "Enable Documentation Builds" ON)

# Link this 'library' to set the c++ standard / compile-time options requested
add_library(project_options INTERFACE)
target_compile_features(project_options INTERFACE cxx_std_17)

# Link this 'library' to use the warnings specified in CompilerWarnings.cmake
add_library(project_warnings INTERFACE)

# standard compiler warnings
include(cmake/CompilerWarnings.cmake)
set_project_warnings(project_warnings)

# sanitizer options if supported by compiler
include(cmake/Sanitizers.cmake)
enable_sanitizers(project_options)

# cppcheck shouldn't validate cpputest since it's a third-party library
set(CPPCHECK_EXCLUDES "--suppress=*:*/CppUTest/*")
# allow for static analysis options
include(cmake/StaticAnalyzers.cmake)

message("CPPCHECK_EXCLUDES is:${CPPCHECK_EXCLUDES}")
message("CMAKE_CXX_CPPCHECK is:${CMAKE_CXX_CPPCHECK}")

add_subdirectory(src)

if(ENABLE_TESTING)
    enable_testing()
    message("Building Tests.")
    add_subdirectory(test)
endif()

if(ENABLE_DOCS)
    message("Building Docs.")
    add_subdirectory(docs)
endif()
