#!/usr/bin/env bash

for endinnaness in be le; do
  # export path to the compiler.
  export PATH=$PATH:/usr/local/opt/arm${endinnaness}-none-eabi-gcc

  # delete the build directory if it exists.
  rm -rf build

  if [ $endianness == "be" ]; then
    CMAKE_ENDIANNESS="big"
  else
    CMAKE_ENDIANNESS="little"
  fi

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
#rm -rf build
#
#USE_CLANG=1
#OPTIONS=""
#
#if [ $USE_CLANG == 1 ]; then
#  CMAKE_C_COMPILER=$(which clang) \
#  CMAKE_AR=$(which llvm-ar) \
#  CMAKE_OBJCOPY=$(which llvm-objcopy) \
#  CMAKE_OBJDUMP=$(which llvm-objdump)
#  else
#  CMAKE_C_COMPILER=$(which arm-none-eabi-gcc) \
#  CMAKE_AR=$(which arm-none-eabi-ar) \
#  CMAKE_OBJCOPY=$(which arm-none-eabi-objcopy) \
#  CMAKE_OBJDUMP=$(which arm-none-eabi-objdump)
#fi
#
#cmake -H. -Bbuild -DCMAKE_BUILD_TYPE=Debug \
#  -DCMAKE_C_COMPILER=$CMAKE_C_COMPILER \
#  -DCMAKE_AR=$CMAKE_AR \
#  -DCMAKE_OBJCOPY=$CMAKE_OBJCOPY \
#  -DCMAKE_OBJDUMP=$CMAKE_OBJDUMP
#pushd build
#make all
#popd
#-DCMAKE_C_COMPILER=$(which arm-none-eabi-gcc) \
#-DCMAKE_AR=$(which arm-none-eabi-ar) \
#-DCMAKE_OBJCOPY=$(which arm-none-eabi-objcopy) \
#-DCMAKE_OBJDUMP=$(which arm-none-eabi-objdump)