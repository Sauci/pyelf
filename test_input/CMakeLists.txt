cmake_minimum_required(VERSION 3.9)

set(CMAKE_TRY_COMPILE_TARGET_TYPE "STATIC_LIBRARY")

project(pyelf ASM C)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

set(endiannesses "big;little")
foreach(endianness ${endiannesses})
    add_library(dummy_0_${endianness}_endian dummy_0.c)
    target_include_directories(dummy_0_${endianness}_endian
        PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
    target_compile_options(dummy_0_${endianness}_endian
        PRIVATE -m${endianness}-endian
        PRIVATE --target=armv7a-none-eabi)

    add_executable(${endianness}_endian.elf crt0.S main.c)
    target_compile_options(${endianness}_endian.elf
        PRIVATE -m${endianness}-endian
        PRIVATE --target=armv7a-none-eabi)
    target_link_options(${endianness}_endian.elf
        PRIVATE -fuse-ld=lld
        PRIVATE -nodefaultlibs
        PRIVATE --target=armv7a-none-eabi)
    target_link_libraries(${endianness}_endian.elf
        PUBLIC dummy_0_${endianness}_endian)
    set_target_properties(${endianness}_endian.elf PROPERTIES
        LINK_FLAGS "-T${CMAKE_CURRENT_SOURCE_DIR}/linker.ld -Wl,-Map,${CMAKE_CURRENT_SOURCE_DIR}/${endianness}_endian.map"
        LINK_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/linker.ld)

    add_custom_target(${endianness}_endian.bin ALL
        DEPENDS ${endianness}_endian.elf
        COMMAND ${CMAKE_OBJCOPY} -O binary ${endianness}_endian.elf ${endianness}_endian.bin
        WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

    add_custom_target(${endianness}_endian.asm ALL
        DEPENDS ${endianness}_endian.elf
        COMMAND ${CMAKE_OBJDUMP} -D -z ${endianness}_endian.elf > ${endianness}_endian.asm
        WORKING_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
endforeach()
