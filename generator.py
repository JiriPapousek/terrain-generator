from PIL import Image
import random
from collections import deque
import math

def random_pixel(sizex, sizey):
    return random.randint(0,sizex),random.randint(0,sizey),random.randint(0,50), random.randint(0,50)

def normal_random(minim, maxim):
    return random.randint(minim,maxim)

def papi_algorithm(sizex, sizey, randomness):
    """
    Try for creating my own algorithm for generating terrain - it randomly
    picks the value in the image, increases it by another value and than it
    increases values of surrounding elements so they would gradually decline.
    This step is repeated until the terrain is complete.
    """
    heights = [[0 for x in range(sizey+1)] for y in range(sizex+1)]

    for i in range(int(sizex*sizey/100)):
        pix = random_pixel(sizex,sizey)
        r = pix[2]
        h = pix[3]
        for x in range(-r,r):
            for y in range(-r,r):
                if (pix[0]+x >= 0) and (pix[0]+x < sizex) and (pix[1]+y >= 0) and (pix[1]+y < sizey):
                    heights[pix[0] + x][pix[1] + y] += int(h - math.sqrt(abs(x)**2+abs(y)**2)*h/r)
    return heights

def square_avg(coordinates, size_of_step, heights):
    sum = 0
    for x in [-1,1]:
        for y in [-1,1]:
            sum += heights[coordinates[0]+size_of_step*x][coordinates[1]+size_of_step*y]
    return int(sum/4)

def square_step(heights, size_of_step, randomness):
    """
    Uses the size of step to get position of elements, which are supposed to
    be calculated in this step.
    """
    s = size_of_step
    r = randomness
    for x in range(0, int((len(heights)-1)/s/2)):
        for y in range(0, int((len(heights)-1)/s/2)):
            value = square_avg([(2*x+1)*s,(2*y+1)*s], s, heights)
            heights[(2*x+1)*s][(2*y+1)*s] = value + normal_random(-r,r)

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
    """
    Works almost same as the square step, but it is little bit more difficult to get
    position of elements to be changed, because the number of those elements is
    different in every row or column.
    """

    s = size_of_step
    r = randomness

    for x in range(0, int((len(heights)-1)/s/2 + 1)):
        for y in range(0, int((len(heights)-1)/s/2)):
            value = diamond_avg([2*x*s, (2*y+1)*s], s, heights)
            heights[2*x*s][(2*y+1)*s] = value + normal_random(-r,r)


    for x in range(0, int((len(heights)-1)/s/2)):
        for y in range(0, int((len(heights)-1)/s/2 + 1)):
            value = diamond_avg([(2*x+1)*s, 2*y*s], s, heights)
            heights[(2*x+1)*s][2*y*s] = value + normal_random(-r,r)


def diamond_square_algorithm(sizex, sizey, randomness):
    """
    Function implementing the diamond-square (or also called midpoint
    displacement) algorithm.
    """

    #Pick longer dimension of the image, find n for which is 2**n + 1 bigger
    #than this dimension, and create two-dimensional list of that size (because
    #it is much simpler to generate terrain for these parameters).

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

    heights = [[None for y in range(size)] for x in range(size)]

    #Set initial values in corners of matrix.
    for x in range(2):
        for y in range(2):
            heights[x * (len(heights)-1)][y *(len(heights[0])-1)] = random.randint(0,255)

    #Repeat square/diamond step until all values in the list are set.
    size_of_step = int((size - 1) / 2)
    while None in [i for x in heights for i in x]:
        square_step(heights, size_of_step, randomness)
        diamond_step(heights, size_of_step, randomness)
        size_of_step = int(size_of_step/2)

    #Reduce the generated list to the size of original image.
    reduced_heights = []
    for x in range(sizex):
        reduced_heights.append([])
        for y in range(sizey):
            reduced_heights[x].append(heights[x][y])
    heights = reduced_heights

    return heights

def mix_algorithm(sizex, sizey, randomness):
    heights1 = diamond_square_algorithm(sizex, sizey, randomness)
    heights2 = papi_algorithm(sizex, sizey, randomness)
    heights = [[None for y in range(sizey)] for x in range(sizex)]

    for x in range(sizex):
        for y in range(sizey):
            heights[x][y] = (heights1[x][y] + heights2[x][y])//2
    return heights

def make_a_bitmap(name, sizex, sizey, randomness, algorithm):
    """
    Function generates image of given size with diamond-square algorithm
    and saves it as .jpg file with given name.
    """
    img = Image.new('RGB', (sizex, sizey), "black")  # create a new black image
    pixels = img.load()  # create the pixel map

    heights = algorithm(sizex, sizey, randomness)
    for x in range(sizex):
        for y in range(sizey):
            pixels[x, y] = (int(heights[x][y]*0.6), int(heights[x][y]*0.9), int(heights[x][y]*0.6))
    img.show()
    img.save(name + ".jpg")

make_a_bitmap("small", 800, 800, 30, mix_algorithm)
