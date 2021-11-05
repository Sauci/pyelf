#!/usr/bin/env bash
rm -rf build
cmake -H. -Bbuild \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_C_COMPILER=$(which clang) \
    -DCMAKE_AR=$(which llvm-ar) \
    -DCMAKE_OBJCOPY=$(which llvm-objcopy) \
    -DCMAKE_OBJDUMP=$(which llvm-objdump)
pushd build
make all
popd
