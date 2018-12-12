#!/usr/bin/env bash
cmake -H. -Bbuild -DCMAKE_C_COMPILER="/usr/local/gcc-arm-none-eabi-7-2017-q4-major/bin/arm-none-eabi-gcc" \
    -DCMAKE_C_COMPILER_WORKS=1
