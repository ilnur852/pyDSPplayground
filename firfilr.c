#include "stdio.h"
#include "math.h"

int main(){
    double lin[256];
    lin[0] =0;
    double sin_wave[256];
    __uint8_t i = 0;


    for (i=0;i<255;i++)
    {
        lin[i+1] = lin[i] + 1;
        //printf("%f \n", lin[i]);
        sin_wave[i] = sin(lin[i]);
        //printf("%f \n", sin_wave[i]);
    };
};
