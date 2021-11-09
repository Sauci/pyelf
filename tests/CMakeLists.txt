cmake_minimum_required(VERSION 3.9)

set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")

project(pyelf ASM C)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

add_library(dummy_0_${CMAKE_ENDIANNESS}_endian dummy_0.c)
target_include_directories(dummy_0_${CMAKE_ENDIANNESS}_endian
    PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_compile_options(dummy_0_${CMAKE_ENDIANNESS}_endian
    PRIVATE -m${CMAKE_ENDIANNESS}-endian
    PRIVATE -march=armv7-r
    )

add_executable(${CMAKE_ENDIANNESS}_endian.elf crt0.S main.c)
target_compile_options(${CMAKE_ENDIANNESS}_endian.elf
    PRIVATE -m${CMAKE_ENDIANNESS}-endian
    PRIVATE -march=armv7-r
    )
target_link_options(${CMAKE_ENDIANNESS}_endian.elf
    PRIVATE -nostartfiles
    PRIVATE -nodefaultlibs
    PRIVATE -march=armv7-r
    )
target_link_libraries(${CMAKE_ENDIANNESS}_endian.elf
    PUBLIC dummy_0_${CMAKE_ENDIANNESS}_endian)
set_target_properties(${CMAKE_ENDIANNESS}_endian.elf PROPERTIES
    LINK_FLAGS "-T${CMAKE_CURRENT_SOURCE_DIR}/linker.ld -Wl,-Map,${CMAKE_CURRENT_SOURCE_DIR}/${CMAKE_ENDIANNESS}_endian.map"
    LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker.ld)

add_custom_target(${CMAKE_ENDIANNESS}_endian.bin ALL
    DEPENDS ${CMAKE_ENDIANNESS}_endian.elf
    COMMAND ${CMAKE_OBJCOPY} -O binary ${CMAKE_ENDIANNESS}_endian.elf ${CMAKE_ENDIANNESS}_endian.bin
    WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

add_custom_target(${CMAKE_ENDIANNESS}_endian.asm ALL
    DEPENDS ${CMAKE_ENDIANNESS}_endian.elf
    COMMAND ${CMAKE_OBJDUMP} -D -z ${CMAKE_ENDIANNESS}_endian.elf > ${CMAKE_ENDIANNESS}_endian.asm
    WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
