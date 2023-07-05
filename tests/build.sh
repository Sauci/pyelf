#!/usr/bin/env bash

rm -rf build

# build the project using the big endian toolchain.
cmake -H. -Bbuild -DCMAKE_C_COMPILER=/usr/local/bin/armeb-none-eabi-gcc/bin/armeb-none-eabi-gcc \
-DCMAKE_BUILD_TYPE=debug \
-DCMAKE_AR=/usr/local/bin/armeb-none-eabi-gcc/bin/armeb-none-eabi-ar \
-DCMAKE_OBJCOPY=/usr/local/bin/armeb-none-eabi-gcc/bin/armeb-none-eabi-objcopy \
-DCMAKE_OBJDUMP=/usr/local/bin/armeb-none-eabi-gcc/bin/armeb-none-eabi-objdump \
-DENDIANNESS=big
pushd build
make all
popd

rm -rf build

# build the project using the little endian toolchain.
cmake -H. -Bbuild -DCMAKE_C_COMPILER=/usr/local/bin/armel-none-eabi-gcc/bin/arm-none-eabi-gcc \
-DCMAKE_BUILD_TYPE=debug \
-DCMAKE_AR=/usr/local/bin/armel-none-eabi-gcc/bin/arm-none-eabi-ar \
-DCMAKE_OBJCOPY=/usr/local/bin/armel-none-eabi-gcc/bin/arm-none-eabi-objcopy \
-DCMAKE_OBJDUMP=/usr/local/bin/armel-none-eabi-gcc/bin/arm-none-eabi-objdump \
-DENDIANNESS=little
pushd build
make all
popd

rm -rf build
