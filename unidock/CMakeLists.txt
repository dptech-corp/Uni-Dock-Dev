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
option(UNIDOCK_LINK_STATIC "Link static libraries" OFF)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
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

add_compile_definitions(UNIDOCK_VERSION="v${PROJECT_VERSION}")

find_package(OpenMP REQUIRED) # OpenMP only required in main.cpp
find_package(Boost 1.72 REQUIRED COMPONENTS system thread serialization
                                            filesystem program_options timer)

# set boost properties
set(Boost_USE_STATIC_LIBS ${UNIDOCK_LINK_STATIC})

add_subdirectory(src)
