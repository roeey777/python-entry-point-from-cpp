# from here:
#
# lint_cmake: -linelength
# https://github.com/lefticus/cppbestpractices/blob/master/02-Use_the_Tools_Available.md
#

function(set_project_warnings project_name)
    option(WARNINGS_AS_ERRORS "Treat compiler warnings as errors" TRUE)
    set(CLANG_WARNINGS
        -Wall
        -Wextra # reasonable and standard
        -Wshadow # warn the user if a variable declaration shadows one from a
                # parent context
        -Wnon-virtual-dtor # warn the user if a class with virtual functions has
                            # a non-virtual destructor. This helps catch hard to
                            # track down memory errors
        -Wold-style-cast # warn for c-style casts
        -Wcast-align # warn for potential performance problem casts
        -Wunused # warn on anything being unused
        -Woverloaded-virtual # warn if you overload (not override) a virtual
                            # function
        -Wpedantic # warn if non-standard C++ is used
        -Wconversion # warn on type conversions that may lose data
        -Wsign-conversion # warn on sign conversions
        -Wnull-dereference # warn if a null dereference is detected
        -Wdouble-promotion # warn if float is implicit promoted to double
        -Wformat=2 # warn on security issues around functions that format output
                    # (ie printf)
    )

    if(WARNINGS_AS_ERRORS)
        set(CLANG_WARNINGS ${CLANG_WARNINGS} -Werror)
    endif()

    set(GCC_WARNINGS
        ${CLANG_WARNINGS}
        -Wmisleading-indentation # warn if identation implies blocks where
                                    # blocks do not exist
        -Wduplicated-cond # warn if if / else chain has duplicated conditions
        -Wduplicated-branches # warn if if / else branches have duplicated code
        -Wlogical-op # warn about logical operations being used where bitwise
                    # were probably wanted
        -Wuseless-cast # warn if you perform a cast to the same type
    )

    if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
	if(NOT ENABLE_CLANG_TIDY)
	    # even if the compiler is GNU clang-tidy would complain...
            set(PROJECT_WARNINGS ${GCC_WARNINGS})
	endif()
    elseif(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        set(PROJECT_WARNINGS ${CLANG_WARNINGS})
    else()
        message(WARNING "Compiler not recognized - cannot set warnings")
    endif()

    target_compile_options(${project_name} INTERFACE ${PROJECT_WARNINGS})
endfunction()
