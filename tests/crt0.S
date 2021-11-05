.global bootloader
.global main

.arm
.section .code.vector
_vector:
    ldr     pc, = bootloader

.arm
.section .code.boot
bootloader:
    mov     r0, #0 // argc
    mov     r1, #0 // argv
    ldr     pc, = main
