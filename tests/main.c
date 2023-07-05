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

typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;

struct dummy_struct_type {
	unsigned char field_uint8;
	unsigned short field_uint16;
	unsigned int field_uint32;
	signed char field_int8;
	signed short field_int16;
	signed int field_int32;
	u8 field_u8;
	u16 field_u16;
	u32 field_u32;
	s8 field_s8;
	s16 field_s16;
	s32 field_s32;
	unsigned short bit_field_0_size_1 : 1;
	unsigned short bit_field_1_size_2 : 2;
	unsigned short bit_field_2_size_3 : 3;
	unsigned short bit_field_3_size_4 : 4;
	unsigned short bit_field_4_size_6 : 6;
	struct {
		unsigned int field_uint8_nesting_0;
		struct {
			signed int field_uint16_nesting_1[5][4][3][2][1];
		};
	};
};

__attribute__((section(".undefined_size")))
struct dummy_struct_type dummy_struct = {};

typedef struct {
	unsigned char field_uint8;
	unsigned short field_uint16;
	unsigned int field_uint32;
	signed char field_int8;
	signed short field_int16;
	signed int field_int32;
} dummy_typedef_struct_type;

__attribute__((section(".undefined_size")))
dummy_typedef_struct_type dummy_typedef_struct;

typedef enum {
	e_1 = 0,
	e_2 = 1,
	e_3 = 3
} dummy_typedef_enum_type;

__attribute__((section(".undefined_size")))
dummy_typedef_enum_type dummy_typedef_enum;

int main(int argc, char *argv[])
{
    dummy_0_fcn();

    return 0;
}
