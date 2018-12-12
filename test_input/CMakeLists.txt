cmake_minimum_required(VERSION 3.9)

project(pyelf C)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(little_endian.elf main.c)
target_compile_options(little_endian.elf
    PRIVATE -mlittle-endian
    PRIVATE -nostdlib
    PRIVATE -march=armv7-a)
target_link_options(little_endian.elf
    PRIVATE -mlittle-endian
    PRIVATE -nostdlib)

add_executable(big_endian.elf main.c)
target_compile_options(big_endian.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib
    PRIVATE -march=armv7-a)
target_link_options(big_endian.elf
    PRIVATE -mbig-endian
    PRIVATE -nostdlib)
