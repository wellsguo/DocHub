#include <stdio.h>
#include "color.h"
 
 
int main()
{
    printf("\033[31m ####----->> \033[32m" "hello\n" "\033[m");
    printf( LIGHT_CYAN "current function is %s " GREEN " file line is %d\n" NONE,
        __FUNCTION__, __LINE__ );
    fprintf(stderr, RED "current function is %s " BLUE " file line is %d\n" NONE,
        __FUNCTION__, __LINE__ );
        return 0;
}