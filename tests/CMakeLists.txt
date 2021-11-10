cmake_minimum_required(VERSION 3.9)

set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")

project(pyelf ASM C)

find_program(SREC_CAT NAMES srec_cat)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_compile_options(-g3 -gdwarf -m${ENDIANNESS}-endian -march=armv7-r)

add_library(dummy_0_${ENDIANNESS}_endian dummy_0.c)

target_include_directories(dummy_0_${ENDIANNESS}_endian
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

add_executable(${ENDIANNESS}_endian.elf crt0.S main.c)

target_link_options(${ENDIANNESS}_endian.elf
    PRIVATE -nostartfiles
    PRIVATE -nodefaultlibs)

target_link_libraries(${ENDIANNESS}_endian.elf
    PUBLIC dummy_0_${ENDIANNESS}_endian)

set_target_properties(${ENDIANNESS}_endian.elf PROPERTIES
    LINK_FLAGS "-T${CMAKE_CURRENT_SOURCE_DIR}/linker.ld -Wl,-Map,${CMAKE_CURRENT_SOURCE_DIR}/${ENDIANNESS}_endian.map"
    LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker.ld)

add_custom_target(${ENDIANNESS}_endian.bin ALL
    DEPENDS ${ENDIANNESS}_endian.elf
    COMMAND ${CMAKE_OBJCOPY} -O binary ${ENDIANNESS}_endian.elf ${ENDIANNESS}_endian.bin
    WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

add_custom_target(${ENDIANNESS}_endian.asm ALL
    DEPENDS ${ENDIANNESS}_endian.elf
    COMMAND ${CMAKE_OBJDUMP} -D -z ${ENDIANNESS}_endian.elf > ${ENDIANNESS}_endian.asm
    WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
