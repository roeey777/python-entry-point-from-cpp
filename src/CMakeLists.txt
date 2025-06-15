set(POC_VERSION 1.0.0)

find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)
find_package(spdlog REQUIRED)

add_library(Poc poc.cpp)
add_library(Poc::Poc ALIAS Poc)

set_target_properties(Poc PROPERTIES EXPORT_NAME Poc)
target_include_directories(
    Poc PUBLIC $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
                $<INSTALL_INTERFACE:include>)

target_link_libraries(Poc PRIVATE project_options project_warnings
                          PUBLIC spdlog::spdlog pybind11::embed)

# Install
include(GNUInstallDirs)
message(STATUS "Generating install")
set(PROJECT_CONFIG_IN "${PROJECT_SOURCE_DIR}/cmake/PocConfig.cmake.in")
set(PROJECT_CONFIG_OUT "${CMAKE_CURRENT_BINARY_DIR}/PocConfig.cmake")
set(CONFIG_TARGETS_FILE "PocConfigTargets.cmake")
set(VERSION_FILE "${CMAKE_CURRENT_BINARY_DIR}/PocConfigVersion.cmake")
set(INSTALL_CONFIG_DIR "${CMAKE_INSTALL_LIBDIR}/cmake/Poc")
set(PC_INSTALL_DIR "${CMAKE_INSTALL_LIBDIR}/pkgconfig")
set(PC_FILE "${CMAKE_BINARY_DIR}/${PROJECT_NAME}.pc")

# Install the library and add the target to export-set
install(
    TARGETS Poc project_options project_warnings
    EXPORT PocTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

# Install public headers
install(DIRECTORY ${PROJECT_SOURCE_DIR}/include/
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# ----------------------------------------------------------------------------
# Install pkg-config file
# ----------------------------------------------------------------------------
get_target_property(PKG_CONFIG_DEFINES Poc INTERFACE_COMPILE_DEFINITIONS)
string(REPLACE ";" " -D" PKG_CONFIG_DEFINES "${PKG_CONFIG_DEFINES}")
string(CONCAT PKG_CONFIG_DEFINES "-D" "${PKG_CONFIG_DEFINES}")
configure_file("${PROJECT_SOURCE_DIR}/cmake/poc.pc.in" "${PC_FILE}" @ONLY)
install(FILES "${PC_FILE}" DESTINATION "${PC_INSTALL_DIR}")

# Install Targets.cmake file
install(
    EXPORT PocTargets
    FILE PocTargets.cmake
    NAMESPACE Poc::
    DESTINATION ${INSTALL_CONFIG_DIR})

# Create PocConfigVersion.cmake file
include(CMakePackageConfigHelpers)
write_basic_package_version_file(
    ${VERSION_FILE}
    VERSION ${POC_VERSION}
    COMPATIBILITY SameMajorVersion)

# Create PocConfig.cmake file
configure_package_config_file(${PROJECT_CONFIG_IN} ${PROJECT_CONFIG_OUT}
                              INSTALL_DESTINATION ${INSTALL_CONFIG_DIR})

# Install the config, configversion and custom find modules
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/PocConfig.cmake
              ${CMAKE_CURRENT_BINARY_DIR}/PocConfigVersion.cmake
        DESTINATION ${INSTALL_CONFIG_DIR})

# Install typing stub into site-packages for future plugins type annotation.
install(FILES
            ${CMAKE_CURRENT_SOURCE_DIR}/poc/typing.py
            ${CMAKE_CURRENT_SOURCE_DIR}/poc/__init__.py
	    ${CMAKE_CURRENT_SOURCE_DIR}/poc/py.typed
        DESTINATION ${Python3_SITELIB}/poc/)

