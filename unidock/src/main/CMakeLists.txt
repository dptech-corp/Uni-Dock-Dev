cmake_minimum_required(VERSION 3.16)

project(unidock)
set(UNIDOCK_MAIN_BIN
    ${PROJECT_NAME}
    PARENT_SCOPE)

add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(
  ${PROJECT_NAME}
  Boost::system
  Boost::thread
  Boost::serialization
  Boost::filesystem
  Boost::program_options
  Boost::timer
  OpenMP::OpenMP_CXX
  ${UNIDOCK_MAIN_LIB}
  ${UNIDOCK_CUDA_LIB})
# For detecting CUDA memory size
target_include_directories(
  ${PROJECT_NAME} PRIVATE ${CMAKE_CUDA_TOOLKIT_INCLUDE_DIRECTORIES}
                          ${Boost_INCLUDE_DIRS})

install(PROGRAMS ${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME} TYPE BIN)
