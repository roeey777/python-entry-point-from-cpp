if (DEFINED ENV{VIRTUAL_ENV})
    # prioritize the python interpreter of the virtual environment, even over conda's
    # own python interpreter. this is required for integration with tox where cmake
    # would find all the C++ packages in conda's environment while installing
    # the python files into tox's virtual environment (found dynamically by cmake).
    set(Python3_EXECUTABLE "$ENV{VIRTUAL_ENV}/bin/python")
    find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
else()
    find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
endif()

message(STATUS "Found Python interpreter: ${Python3_INTERPRETER}")
message(STATUS "Python version: ${Python3_VERSION}")
message(STATUS "Python executable path: ${Python3_EXECUTABLE}")
message(STATUS "Found Python3 site-packages at: ${Python3_SITELIB}")

# Install
include(GNUInstallDirs)
set(VERSION_PY_FILE "${CMAKE_BINARY_DIR}/version.py")

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/version.py.in" "${VERSION_PY_FILE}" @ONLY)

# Install typing stub into site-packages for future plugins type annotation.
install(FILES
            ${CMAKE_CURRENT_SOURCE_DIR}/typing.py
            ${CMAKE_CURRENT_SOURCE_DIR}/__init__.py
	    ${CMAKE_CURRENT_SOURCE_DIR}/py.typed
	    ${VERSION_PY_FILE}
        DESTINATION ${Python3_SITELIB}/poc/)

# install dist-info for the poc package so it would be recognizable by pip
set(METADATA_FILE "${CMAKE_BINARY_DIR}/METADATA")
set(RECORD_FILE "${CMAKE_BINARY_DIR}/RECORD")

string(TOLOWER "${PROJECT_NAME}" PROJECT_NAME_LOWERCASE)

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/METADATA.in" "${METADATA_FILE}" @ONLY)

# compute sha256 & size in bytes of python files as well as METADATA & INSTALLER files.
file(SHA256 "${METADATA_FILE}" METADATA_SHA256)
file(SIZE "${METADATA_FILE}" METADATA_BYTES)
file(SHA256 "${CMAKE_CURRENT_SOURCE_DIR}/INSTALLER" INSTALLER_SHA256)
file(SIZE "${CMAKE_CURRENT_SOURCE_DIR}/INSTALLER" INSTALLER_BYTES)
file(SHA256 "${CMAKE_CURRENT_SOURCE_DIR}/typing.py" TYPING_PY_SHA256)
file(SIZE "${CMAKE_CURRENT_SOURCE_DIR}/typing.py" TYPING_PY_BYTES)
file(SHA256 "${VERSION_PY_FILE}" VERSION_PY_SHA256)
file(SIZE "${VERSION_PY_FILE}" VERSION_PY_BYTES)
file(SHA256 "${CMAKE_CURRENT_SOURCE_DIR}/__init__.py" INIT_PY_SHA256)
file(SIZE "${CMAKE_CURRENT_SOURCE_DIR}/__init__.py" INIT_PY_BYTES)

# now we can configure the RECORD.in file.
configure_file("${CMAKE_CURRENT_SOURCE_DIR}/RECORD.in" "${RECORD_FILE}" @ONLY)
install(FILES
            "${CMAKE_CURRENT_SOURCE_DIR}/INSTALLER"
	    "${METADATA_FILE}"
	    "${RECORD_FILE}"
	DESTINATION ${Python3_SITELIB}/poc-${POC_VERSION}.dist-info/)
