#!/usr/bin/env bash

for endinnaness in big little; do
  # export path to the compiler.
  export PATH=$PATH:/usr/local/opt/arm${endinnaness}-none-eabi-gcc

  # delete the build directory if it exists.
  rm -rf build

  # build the project using either the big or the little endian toolchain.
  cmake -H. -Bbuild -DCMAKE_C_COMPILER=$(which arm-none-eabi-gcc) \
  -DCMAKE_AR=$(which arm-none-eabi-ar) \
  -DCMAKE_OBJCOPY=$(which arm-none-eabi-objcopy) \
  -DCMAKE_OBJDUMP=$(which arm-none-eabi-objdump) \
  -DCMAKE_ENDIANNESS=$CMAKE_ENDIANNESS
  pushd build
  make all
  popd
done
