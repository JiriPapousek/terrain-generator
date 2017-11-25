from PIL import Image
import random
from collections import deque

def random_pixel(sizex,sizey):
    return random.randint(0,sizex),random.randint(0,sizey),random.randint(0,20)

def papi_algorithm(sizex,sizey):
    heights = [[0 for x in range(sizey+1)] for y in range(sizex+1)]

    for i in range(int(sizex*sizey/10)):
        pix = random_pixel(sizex,sizey)
        for r in range(pix[2]):
            for x in range(-r,r):
                for y in range(-r,r):
                    ran = random.randint(0, 2)
                    if (pix[0]+x >= 0) and (pix[0]+x < sizex) and (pix[1]+y >= 0) and (pix[1]+y < sizey):
                        if ran==0:
                            heights[pix[0]+x][pix[1]+y] += int((r - abs(x))/5)
                        elif ran==1:
                            heights[pix[0] + x][pix[1] + y] += int((r - abs(y))/5)
                        else:
                            heights[pix[0] + x][pix[1] + y] += int((r - abs(x) - abs(y))/5)
    return heights

def square_avg(coordinates, size_of_step, heights):
    sum = 0
    for x in [-1,1]:
        for y in [-1,1]:
            print(coordinates[0]+size_of_step*x, ":",coordinates[1]+size_of_step*y)
            sum += heights[coordinates[0]+size_of_step*x][coordinates[1]+size_of_step*y]
    return int(sum/4)

def square_step(heights, size_of_step, randomness):
    for x in range(0, int((len(heights)-1)/size_of_step/2)):
        for y in range(0, int((len(heights)-1)/size_of_step/2)):
            value = square_avg([(2*x+1)*size_of_step,(2*y+1)*size_of_step], size_of_step, heights)
            heights[(2*x+1)*size_of_step][(2*y+1)*size_of_step] = value + random.randint(-randomness,randomness)

def diamond_avg(coordinates, size_of_step, heights):
    sum = 0
    number_of_addings = 0
    for i in [-1,1]:
        if (coordinates[0] + i * size_of_step >= 0) and (coordinates[0] + i * size_of_step < len(heights)-1):
            sum += heights[coordinates[0]+i*size_of_step][coordinates[1]]
            number_of_addings += 1
    for i in [-1,1]:
        if (coordinates[1]+i*size_of_step >= 0) and (coordinates[1] + i * size_of_step < len(heights)):
            sum += heights[coordinates[0]][coordinates[1]+i*size_of_step]
            number_of_addings += 1
    return int(sum/number_of_addings)

def diamond_step(heights, size_of_step, randomness):

    for x in range(0, int((len(heights)-1)/size_of_step/2 + 1)):
        for y in range(0, int((len(heights)-1)/size_of_step/2)):
            value = diamond_avg([2*x*size_of_step, (2*y+1)*size_of_step], size_of_step, heights)
            heights[2*x*size_of_step][(2*y+1)*size_of_step] = value + random.randint(-randomness,randomness)


    for x in range(0, int((len(heights)-1)/size_of_step/2)):
        for y in range(0, int((len(heights)-1)/size_of_step/2 + 1)):
            value = diamond_avg([(2*x+1)*size_of_step, 2*y*size_of_step], size_of_step, heights)
            heights[(2*x+1)*size_of_step][2*y*size_of_step] = value + random.randint(-randomness,randomness)


def diamond_square_algorithm(size, randomness):
    heights = [[None for y in range(size)] for x in range(size)]

    #Sets initial values in corners of matrix.
    for x in range(2):
        for y in range(2):
            heights[x * (len(heights)-1)][y *(len(heights[0])-1)] = random.randint(0,255)

    size_of_step = int((size - 1) / 2)
    while None in [i for x in heights for i in x]:
        square_step(heights, size_of_step, randomness)
        diamond_step(heights, size_of_step, randomness)
        print("...")
        for i in heights:
            print(i)
        print("...")
        size_of_step = int(size_of_step/2)

    return heights

def make_a_bitmap(name, sizex, sizey,randomness):
    if sizex>sizey:
        size = sizex
    else:
        size = sizey

    power = 0
    size = size - 1
    while size>1:
        size = size/2
        power += 1
    size = 2**power + 1

    img = Image.new('RGB', (sizex, sizey), "black")  # create a new black image
    pixels = img.load()  # create the pixel map

    heights = diamond_square_algorithm(size,randomness)
    for x in range(sizex):
        for y in range(sizey):
            grey = int(heights[x][y])
            pixels[x,y] = (int(grey),int(grey/1.5),int(grey/9))
    img.show()
    img.save(name + ".jpg")

make_a_bitmap("map",1600,900,20)