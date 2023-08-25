cmake_minimum_required(VERSION 3.16)

project(libunidock)
set(UNIDOCK_MAIN_LIB
    ${PROJECT_NAME}
    PARENT_SCOPE)

add_library(
  ${PROJECT_NAME} OBJECT
  ad4cache.cpp
  cache.cpp
  non_cache.cpp
  conf_independent.cpp
  coords.cpp
  grid.cpp
  szv_grid.cpp
  model.cpp
  mutate.cpp
  parallel_mc.cpp
  parse_pdbqt.cpp
  quasi_newton.cpp
  quaternion.cpp
  random.cpp
  utils.cpp
  vina.cpp
  precalculate.h)

target_include_directories(${PROJECT_NAME} PUBLIC .)
