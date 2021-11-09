MEMORY
{
    FLASH_ECC_BANK_0_SECTOR_0 (x) :  ORIGIN = 0x00000000, LENGTH = 16K
    RAM_ECC (rwx) :                  ORIGIN = 0x08400000, LENGTH = 512K
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
        . = ALIGN(0x04);
    } > FLASH_ECC_BANK_0_SECTOR_0
    .rodata :
    {
        *(.rodata)
        . = ALIGN(0x04);
    } > FLASH_ECC_BANK_0_SECTOR_0
    .text :
    {
        *(.text)
        . = ALIGN(0x04);
    } > FLASH_ECC_BANK_0_SECTOR_0
    .data :
    {
        *(.data)
        . = ALIGN(0x04);
    } > FLASH_ECC_BANK_0_SECTOR_0
    .bss :
    {
        *(.bss)
        *(COMMON)
        . = ALIGN(0x04);
    } > RAM_ECC
    /DISCARD/ :
    {
        *(.comment)
        *(.ARM.*)
    }
}
