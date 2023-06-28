MEMORY
{
    FLASH (rx)  : ORIGIN = 0x00000000, LENGTH = 16K
    RAM   (rwx) : ORIGIN = 0x08400000, LENGTH = 512K
}


ENTRY(bootloader);

SECTIONS
{
    .code 0x00000000 :
    {
        *(.code.vector)
        . = ABSOLUTE(0x00000020);
        *(.code.boot);
        . = ALIGN(0x04);
        *(.code);
    } > FLASH
    .rodata :
    {
        . = ALIGN(0x04);
        *(.rodata)
    } > FLASH
    .text :
    {
        . = ALIGN(0x04);
        *(.text)
    } > FLASH
    .data :
    {
        . = ALIGN(0x04);
        *(.data)
    } > FLASH
    .init_lma :
    {
        . = ALIGN(0x04);
    } > FLASH = 0xFF
    .init_vma : AT(ADDR(.init_lma))
    {
        *(.unsigned.8)
        . = ALIGN(0x04);
        *(.unsigned.16)
        . = ALIGN(0x04);
        *(.unsigned.32)
        . = ALIGN(0x04);
        *(.signed.8)
        . = ALIGN(0x04);
        *(.signed.16)
        . = ALIGN(0x04);
        *(.signed.32)
        . = ALIGN(0x04);
        *(.undefined_size)
        . = ALIGN(0x04);
    } > RAM
    .bss (NOLOAD) :
    {
        *(.bss)
        *(COMMON)
        . = ALIGN(0x04);
    } > RAM
    .free_flash_lma ADDR(.init_lma) + SIZEOF(.init_vma) :
    {
        BYTE(0xFF);
        . = ABSOLUTE(LENGTH(FLASH));
    } > FLASH = 0xFF
    /DISCARD/ :
    {
        *(.comment)
        *(.ARM.*)
    }
}
