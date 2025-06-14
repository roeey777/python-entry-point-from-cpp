# Look for an executable called sphinx-build
find_program(SPHINX_EXECUTABLE
            NAMES sphinx-build
            DOC "Path to sphinx-build executable")

message(STATUS "Found sphinx-build at: ${SPHINX_EXECUTABLE}")

include(FindPackageHandleStandardArgs)

# Handle standard arguments to find_package like REQUIRED and QUIET
find_package_handle_standard_args(
        Sphinx
        "Failed to find sphinx-build executable"
        SPHINX_EXECUTABLE)

message(STATUS "Sphinx_FOUND: ${Sphinx_FOUND}")

if(Sphinx_FOUND)
  mark_as_advanced(SPHINX_EXECUTABLE)
endif()

if(Sphinx_FOUND AND NOT TARGET Sphinx::Sphinx)
  add_executable(Sphinx::Sphinx IMPORTED)
  set_property(TARGET Sphinx::Sphinx
            PROPERTY IMPORTED_LOCATION ${Sphinx_EXECUTABLE})
endif()

