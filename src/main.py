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

def colourbend(redOffset,greenOffset,blueOffset,alphaOffset, randomiseOffset, randomnessAmount):

    if randomiseOffset == True:

        for x in range(0, imgwidth):

            redRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            greenRandomness = random.uniform(-randomnessAmount,randomnessAmount)
            blueRandomness = random.uniform(-randomnessAmount,randomnessAmount)

            for y in range(0, imgheight):

                data[y][x][0] -= redOffset * redRandomness
                data[y][x][1] -= greenOffset * greenRandomness
                data[y][x][2] -= blueOffset * blueRandomness
                data[y][x][3] -= alphaOffset
    else:

        for x in range(0, imgwidth):

            for y in range(0, imgheight):

                redRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1
                greenRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1
                blueRandomness = random.uniform(-randomnessAmount,randomnessAmount) + 1

                data[y][x][0] -= redOffset * redRandomness
                data[y][x][1] -= greenOffset * greenRandomness
                data[y][x][2] -= blueOffset * blueRandomness
                data[y][x][3] -= alphaOffset

def pixelShift(frequency,horizontalOffset):
    for i in range(0,frequency):
        offset = random.randint(horizontalOffset/2,horizontalOffset)
        for y in range(int(i*imgheight/frequency),int((i+1)*imgheight/frequency)):
            for x in range(0,imgwidth):
                if x-offset > 0:
                    data[y][x] = original[y][x-offset]
                else:
                    data[y][x] = original[y][(imgwidth-1) + (x-offset)]

            

    
original = tiff.imread('images/test.tiff')
data = tiff.imread('images/test.tiff')

imgwidth = 1920
imgheight = 1080

print(data.shape)
pixelShift(8,imgwidth/2)
colourbend(255,255,255,0,False,0)


tiff.imwrite('images/test2.tiff', data, photometric='rgb')