#include "dummy_0.h"

__attribute__((section(".unsigned.8")))
unsigned char dummy_var_no_init_uint8;

__attribute__((section(".unsigned.16")))
unsigned short dummy_var_no_init_uint16;

__attribute__((section(".unsigned.32")))
unsigned int dummy_var_no_init_uint32;

__attribute__((section(".signed.8")))
signed char dummy_var_no_init_sint8;

__attribute__((section(".signed.16")))
signed short dummy_var_no_init_sint16;

__attribute__((section(".signed.32")))
signed int dummy_var_no_init_sint32;

int main(int argc, char *argv[])
{
    (void)dummy_var_no_init_uint8;
    (void)dummy_var_no_init_uint16;
    (void)dummy_var_no_init_uint32;

    dummy_0_fcn();

    return 0;
}
