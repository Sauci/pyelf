#include "dummy_0.h"

const int arch_paths_first;

unsigned char dummy_var_no_init_uint8;
unsigned short dummy_var_no_init_uint16;
unsigned int dummy_var_no_init_uint32;
signed char dummy_var_no_init_sint8;
signed short dummy_var_no_init_sint16;
signed int dummy_var_no_init_sint32;

int main(int argc, char *argv[])
{
    (void)dummy_var_no_init_uint8;
    (void)dummy_var_no_init_uint16;
    (void)dummy_var_no_init_uint32;

    dummy_0_fcn();

    return 0;
}
