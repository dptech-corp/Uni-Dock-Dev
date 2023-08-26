cmake_minimum_required(VERSION 3.16)

project(
  Uni-Dock
  VERSION 1.0.0
  DESCRIPTION "GPU-Accelerated Docking with 1000-fold speedup"
  HOMEPAGE_URL "https://github.com/dptech-corp/Uni-Dock"
  LANGUAGES CXX CUDA)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CUDA_STANDARD 14)
set(CMAKE_CUDA_STANDARD_REQUIRED True)

# Options for Uni-Dock
option(
  UNIDOCK_LINK_STATIC
  "Link static libraries. Only support when UNIDOCK_USE_FETCHCONTENT is OFF" ON)
option(UNIDOCK_USE_FETCHCONTENT "Use FetchContent to download dependencies" OFF)

# Set the default build type to Release. If you want to build in Debug mode, run
# cmake with -DCMAKE_BUILD_TYPE=Debug
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# Include FetchContent if the option is ON
if(UNIDOCK_USE_FETCHCONTENT)
  include(FetchContent)
endif()

include(CheckLanguage)
check_language(CUDA)
if(NOT DEFINED CMAKE_CUDA_ARCHITECTURES)
  # https://en.wikipedia.org/wiki/CUDA#GPUs_supported
  set(CMAKE_CUDA_ARCHITECTURES
      60 # P100
      70 # V100
      75 # T4
      80 # A100
      89 # RTX 40
      90 # H100
  )
endif()

find_package(OpenMP REQUIRED) # OpenMP only required in main.cpp

# Make boost available
set(UNIDOCK_BOOST_COMPONENTS system thread serialization filesystem
                             program_options timer)
set(Boost_USE_STATIC_LIBS ${UNIDOCK_LINK_STATIC})
if(UNIDOCK_USE_FETCHCONTENT)
  FetchContent_Declare(
    Boost
    URL https://github.com/boostorg/boost/releases/download/boost-1.83.0/boost-1.83.0.tar.xz
    URL_MD5 526bdefb658b42209e691d48dd750e7a
    DOWNLOAD_EXTRACT_TIMESTAMP TRUE)
  FetchContent_GetProperties(Boost)

  if(NOT boost_POPULATED)
    message(STATUS "Fetching Boost")
    FetchContent_Populate(Boost)

    message(STATUS "Configuring Boost")
    add_subdirectory(${boost_SOURCE_DIR} ${boost_BINARY_DIR} EXCLUDE_FROM_ALL)
  endif()
else()
  # set boost properties
  find_package(Boost 1.72 REQUIRED COMPONENTS ${UNIDOCK_BOOST_COMPONENTS})
endif()

# Get current version from git. If the git command is unavailable or
# git-describe returns error, use the version from CMakeLists.txt
find_package(Git)
if(GIT_EXECUTABLE)
  # Generate a git-describe version string from Git repository tags
  execute_process(
    COMMAND ${GIT_EXECUTABLE} describe --tags --dirty
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE GIT_DESCRIBE_VERSION
    RESULT_VARIABLE GIT_DESCRIBE_ERROR_CODE
    OUTPUT_STRIP_TRAILING_WHITESPACE)
  if(NOT GIT_DESCRIBE_ERROR_CODE)
    set(UNIDOCK_GIT_VERSION ${GIT_DESCRIBE_VERSION})
  endif()
endif()

if(UNIDOCK_GIT_VERSION)
  add_compile_definitions(UNIDOCK_VERSION="v${UNIDOCK_GIT_VERSION}")
else()
  add_compile_definitions(UNIDOCK_VERSION="v${PROJECT_VERSION}")
endif()

add_subdirectory(src)
