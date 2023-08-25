cmake_minimum_required(VERSION 3.16)

project(split)
set(UNIDOCK_SPLIT_BIN
    ${PROJECT_NAME}
    PARENT_SCOPE)

add_executable(${PROJECT_NAME} split.cpp)

target_link_libraries(
  ${PROJECT_NAME}
  Boost::system
  Boost::thread
  Boost::serialization
  Boost::filesystem
  Boost::program_options
  Boost::timer
  ${UNIDOCK_MAIN_LIB}
  ${UNIDOCK_CUDA_LIB})
target_include_directories(${PROJECT_NAME} PRIVATE ${Boost_INCLUDE_DIRS})
