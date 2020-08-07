#include <stdint.h>
#include <stdio.h>

int main (int argc, char **argv) {
    uint64_t rcs = 0;
    asm ("mov %%cs, %0" : "=r" (rcs));
    printf("%d\n", (int) (rcs & 3));
    return 0;
}

