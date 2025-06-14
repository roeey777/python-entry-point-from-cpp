option(ENABLE_CPPCHECK "Enable static analysis with cppcheck" OFF)
option(ENABLE_CLANG_TIDY "Enable static analysis with clang-tidy" OFF)
option(ENABLE_IWYU "Enable static analysis with iwyu (include-what-you-use)" OFF)

if(NOT DEFINED CPPCHECK_EXCLUDES)
  set(CPPCHECK_EXCLUDES
      ""
      CACHE
        STRING
# lint_cmake: -linelength
        "List of files to be excluded from cppcheck validation (useful for third-party libraries)"
  )
endif()

if(ENABLE_CPPCHECK)
  find_program(CPPCHECK cppcheck)
  if(CPPCHECK)
    message(STATUS "Found cppcheck at: ${CPPCHECK}")
    set(CMAKE_CXX_CPPCHECK ${CPPCHECK} --suppress=missingInclude --enable=all
                            ${CPPCHECK_EXCLUDES} --inconclusive)
  else()
    message(SEND_ERROR "cppcheck requested but executable not found")
  endif()
endif()

if(ENABLE_CLANG_TIDY)
  find_program(CLANGTIDY clang-tidy)
  if(CLANGTIDY)
    message(STATUS "Found clang-tidy at: ${CLANGTIDY}")
    # construct the clang-tidy command line
    set(CLANG_TIDY_OPTIONS
        ${CLANGTIDY}
        -extra-arg=-Wno-unknown-warning-option
        -extra-arg=-Wno-ignored-optimization-argument
        -extra-arg=-Wno-unused-command-line-argument
	-warnings-as-errors=*
        -p)
    # set standard
    if(NOT
       "${CMAKE_CXX_STANDARD}"
       STREQUAL
       "")
      if("${CLANG_TIDY_OPTIONS_DRIVER_MODE}" STREQUAL "cl")
        set(CLANG_TIDY_OPTIONS ${CLANG_TIDY_OPTIONS} -extra-arg=/std:c++${CMAKE_CXX_STANDARD})
      else()
        set(CLANG_TIDY_OPTIONS ${CLANG_TIDY_OPTIONS} -extra-arg=-std=c++${CMAKE_CXX_STANDARD})
      endif()
    endif()
  else()
    message(SEND_ERROR "clang-tidy requested but executable not found")
  endif()
endif()

if(ENABLE_IWYU)
  find_program(INCLUDE_WHAT_YOU_USE include-what-you-use)
  if(INCLUDE_WHAT_YOU_USE)
    message(STATUS "Found iwyu (include-what-you-use) at: ${INCLUDE_WHAT_YOU_USE}")
    set(CMAKE_CXX_INCLUDE_WHAT_YOU_USE ${INCLUDE_WHAT_YOU_USE})
  else()
    message(${WARNING_MESSAGE} "include-what-you-use requested but executable not found")
  endif()
endif()
