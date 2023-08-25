cmake_minimum_required(VERSION 3.16)

project(libunidock_cuda)
set(UNIDOCK_CUDA_LIB
    ${PROJECT_NAME}
    PARENT_SCOPE)

add_library(${PROJECT_NAME} OBJECT monte_carlo.cu precalculate.cu)

target_include_directories(${PROJECT_NAME} PUBLIC .)
target_link_libraries(${PROJECT_NAME} PUBLIC ${UNIDOCK_MAIN_LIB})
