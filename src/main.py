import tifffile as tiff
import random
import numpy

def clampSize(n, bound): 
    if n < 0: 
        return 0
    elif n > bound: 
        return bound
    else: 
        return n 

def colourbend(rOffset,gOffset,bOffset,aOffset, randomnessAmount):

    for x in range(0, imgwidth):

        for y in range(0, imgheight):

            rRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            gRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            bRandomness = random.uniform(-randomnessAmount,randomnessAmount)

            data[y][x][0] -= rOffset * rRandomness
            data[y][x][1] -= gOffset * gRandomness
            data[y][x][2] -= bOffset * bRandomness
            data[y][x][3] -= aOffset

def pixelShift(frequency):
    for i in frequency:
        for y in range(i*imgheight/frequency,(i+1)*imgheight/frequency):
            for x in range(0,imgwidth):
                if x-500 > 0:
                    print(x)
                    data[y][x] = original[y][x-500]
                else:
                    data[y][x] = original[y][(imgwidth-1) + (x-500)]

            

    
original = tiff.imread('images/test.tiff')
data = tiff.imread('images/test.tiff')

imgwidth = 1920
imgheight = 1080

print(data.shape)
pixelShift()


tiff.imwrite('images/test2.tiff', data, photometric='rgb')