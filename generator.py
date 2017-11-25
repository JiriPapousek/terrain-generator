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

def avg_square(coordinates, heights):
    sum = 0
    for x in range(2):
        for y in range(2):
            sum += heights[coordinates[2*x+y][0]][coordinates[2*x+y][1]]
    return int(sum/len(coordinates))


def square_step(heights):
    sizex = len(heights)
    sizey = len(heights[0])
    copy_of_heights = [[i for i in x] for x in heights]
    corners = [0, 0, 0, 0]
    while len(corners) == 4:
        corners = []
        for x in range(sizex):
            if len([i for i in copy_of_heights[x] if i != None]):
                for y in range(sizey):
                    if copy_of_heights[x][y] != None:
                        if len(corners) < 2:
                            corners.append((x, y))
                        elif ((len(corners) == 2) and (y == corners[0][1])) or (
                            (len(corners) == 3) and (y == corners[1][1])):
                            corners.append((x, y))
                if len(corners) == 4:
                    break
        if len(corners) == 4:
            new_x = int((corners[0][0] + corners[3][0]) / 2)
            new_y = int((corners[0][1] + corners[3][1]) / 2)
            heights[new_x][new_y] = avg_square(corners, heights)+random.randint(-10,10)
            copy_of_heights[corners[0][0]][corners[0][1]] = None

def avg_diamond(coordinates, heights):
    sum = 0
    for c in coordinates:
            sum += heights[c[0]][c[1]]
    return int(sum/len(coordinates))

def get_intersect_list(heights):
    intersect_list = [[[] for y in range(len(heights[x]))] for x in range(len(heights))]
    for x in range(len(heights)):
        for y in range(len(heights[x])):
            if heights[x][y] != None:
                for inter_x in range(x + 1, len(heights)):
                    if heights[inter_x][y] == None:
                        intersect_list[inter_x][y].append((x,y))
                    else:
                        break
                for inter_x in range(0, x)[::-1]:
                    if heights[inter_x][y] == None:
                        intersect_list[inter_x][y].append((x,y))
                    else:
                        break
                for inter_y in range(0, y)[::-1]:
                    if heights[x][inter_y] == None:
                        intersect_list[x][inter_y].append((x,y))
                    else:
                        break
                for inter_y in range(y + 1, len(heights[x])):
                    if heights[x][inter_y] == None:
                        intersect_list[x][inter_y].append((x,y))
                    else:
                        break
    return intersect_list

def diamond_step(heights):
    intersect_list = get_intersect_list(heights)
    for x in range(len(heights)):
        for y in range(len(heights[x])):
            if len(intersect_list[x][y])>2:
                heights[x][y] = avg_diamond(intersect_list[x][y],heights)+random.randint(-30,30)

def diamond_square_algorithm(sizex,sizey):
    heights = [[None for y in range(sizey)] for x in range(sizex)]

    #Sets initial values in corners of matrix.
    for x in range(2):
        for y in range(2):
            heights[x * (len(heights)-1)][y *(len(heights[0])-1)] = random.randint(0,255)

    while None in [i for x in heights for i in x]:
        square_step(heights)
        diamond_step(heights)

    return heights

def make_a_bitmap(name, sizex, sizey):
    img = Image.new('RGB', (sizex, sizey), "black")  # create a new black image
    pixels = img.load()  # create the pixel map

    heights = diamond_square_algorithm(sizex, sizey)
    for x in range(sizex):
        for y in range(sizey):
            grey = int(heights[x][y])
            pixels[x,y] = (int(grey/1.1),int(grey),int(grey/1.3))
    img.show()
    img.save(name + ".jpg")

make_a_bitmap("map",513,513)