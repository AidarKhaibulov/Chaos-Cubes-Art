import math
from random import randint

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter


def rotMatr(ang):
    mtr = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
    return mtr

def draw_line(x0, y0, x1, y1, image, color):
    # Bresenham's algorithm
    sign_x = 0
    sign_y = 0

    if x1 - x0 > 0:
        sign_x = 1
    elif x1 - x0 < 0:
        sign_x = -1

    if y1 - y0 > 0:
        sign_y = 1
    elif y1 - y0 < 0:
        sign_y = -1

    delta_x = abs(x1 - x0)
    delta_y = abs(y1 - y0)

    if delta_x > delta_y:
        d = delta_x
        dd = delta_y
    else:
        d = delta_y
        dd = delta_x
    x_cur, y_cur = x0, y0
    error = d / 2
    image[y_cur, x_cur] = color

    for i in range(d):
        error -= dd
        if error < 0:
            error += d
            x_cur += sign_x
            y_cur += sign_y
        else:
            if delta_x > delta_y:
                x_cur += sign_x
            else:
                y_cur += sign_y
        image[y_cur, x_cur] = color
cubes_amount=4
first_cube_center=[300,400]
second_cube_center=[500,500]
third_cube_center=[600,600]
fourth_cube_center=[700,700]
#fifth_cube_center=[400,200]
cubes_angle=[1,1,1,1]
width, height = 1000, 1000
count_foursquare = 4
rotation_speed = np.pi
img = np.zeros((width, height, 3), dtype=np.uint8)
animation.ffmpeg_path = 'ffmpeg'
fig = plt.figure(frameon=False)
plt.axis('off')
cubes_speed = [[10, 4], [-10, 14], [5, -10],[-4,-4]]
# ---------------------------------------------------------------
frames = []
for i in range(height):
    for j in range(width):
        img[i][j] = [255, 255, 255]
for frame in range(100):
    first_cube_points = [[first_cube_center[0]-30, first_cube_center[1]+30],
                         [first_cube_center[0]+30, first_cube_center[1]+30],
                         [first_cube_center[0]+30, first_cube_center[1]-30],
                         [first_cube_center[0]-30, first_cube_center[1]-30]]
    second_cube_points = [[second_cube_center[0]-30, second_cube_center[1]+30],
                         [second_cube_center[0]+30, second_cube_center[1]+30],
                         [second_cube_center[0]+30, second_cube_center[1]-30],
                         [second_cube_center[0]-30, second_cube_center[1]-30]]
    third_cube_points = [[third_cube_center[0]-30, third_cube_center[1]+30],
                         [third_cube_center[0]+30, third_cube_center[1]+30],
                         [third_cube_center[0]+30, third_cube_center[1]-30],
                         [third_cube_center[0]-30, third_cube_center[1]-30]]
    fourth_cube_points = [[fourth_cube_center[0] - 30, fourth_cube_center[1] + 30],
                         [fourth_cube_center[0] + 30, fourth_cube_center[1] + 30],
                         [fourth_cube_center[0] + 30, fourth_cube_center[1] - 30],
                         [fourth_cube_center[0] - 30, fourth_cube_center[1] - 30]]
    cubes_vertices = [first_cube_points, second_cube_points, third_cube_points,fourth_cube_points]
    cubes_centers=[first_cube_center,second_cube_center,third_cube_center,fourth_cube_center]

    # scene refreshing
    for i in range(height):
        for j in range(width):
            img[i][j] = [255, 255, 255]

    # out of canvas cases
    for i in range(cubes_amount):
        if cubes_centers[i][0] < math.sqrt(2) * 70 or cubes_centers[i][0] > width - math.sqrt(2) * 40:
            cubes_speed[i][0] *= -1
            cubes_angle[i] *= -1
        if cubes_centers[i][1] < math.sqrt(2) * 70 or cubes_centers[i][1] > width - math.sqrt(2) * 40:
            cubes_speed[i][1] *= -1
            cubes_angle[i] *= -1

    # collision cases
    for i in range(cubes_amount):
        for j in range(i+1,cubes_amount):
            if np.sqrt(((cubes_centers[i][0] - cubes_centers[j][0]) ** 2) + ((cubes_centers[i][1] - cubes_centers[j][1]) ** 2))<math.sqrt(2)*60:
                cubes_speed[i][0] *= -1
                cubes_speed[i][1] *= -1
                cubes_angle[i] *= -1
                cubes_speed[j][0] *= -1
                cubes_speed[j][1] *= -1
                cubes_angle[j] *= -1
    # cubes shifting
    for i in range(cubes_amount):
        cubes_centers[i][0]+=cubes_speed[i][0]
        cubes_centers[i][1]+=cubes_speed[i][1]
    for i in range(cubes_amount):
        cubes_vertices[i][0][0]-=cubes_centers[i][0]
        cubes_vertices[i][0][1]-=cubes_centers[i][1]
        cubes_vertices[i][1][0] -= cubes_centers[i][0]
        cubes_vertices[i][1][1] -= cubes_centers[i][1]
        cubes_vertices[i][2][0] -= cubes_centers[i][0]
        cubes_vertices[i][2][1] -= cubes_centers[i][1]
        cubes_vertices[i][3][0] -= cubes_centers[i][0]
        cubes_vertices[i][3][1] -= cubes_centers[i][1]
        cubes_vertices[i]=cubes_vertices[i] @ rotMatr(rotation_speed * cubes_angle[i])
        cubes_vertices[i][0][0] += cubes_centers[i][0]
        cubes_vertices[i][0][1] += cubes_centers[i][1]
        cubes_vertices[i][1][0] += cubes_centers[i][0]
        cubes_vertices[i][1][1] += cubes_centers[i][1]
        cubes_vertices[i][2][0] += cubes_centers[i][0]
        cubes_vertices[i][2][1] += cubes_centers[i][1]
        cubes_vertices[i][3][0] += cubes_centers[i][0]
        cubes_vertices[i][3][1] += cubes_centers[i][1]
    rotation_speed+=0.07
    # cubes drawing
    for i in range(cubes_amount):
        draw_line(int(cubes_vertices[i][0][0]),int(cubes_vertices[i][0][1]),int(cubes_vertices[i][1][0]),int(cubes_vertices[i][1][1]),img,[0,0,0])
        draw_line(int(cubes_vertices[i][1][0]),int(cubes_vertices[i][1][1]),int(cubes_vertices[i][2][0]),int(cubes_vertices[i][2][1]),img,[0,0,0])
        draw_line(int(cubes_vertices[i][2][0]),int(cubes_vertices[i][2][1]),int(cubes_vertices[i][3][0]),int(cubes_vertices[i][3][1]),img,[0,0,0])
        draw_line(int(cubes_vertices[i][3][0]),int(cubes_vertices[i][3][1]),int(cubes_vertices[i][0][0]),int(cubes_vertices[i][0][1]),img,[0,0,0])


    im = plt.imshow(img.swapaxes(0, 1), origin='lower')
    frames.append([im])
# ---------------------------------------------------------------
ani = animation.ArtistAnimation(fig, frames, interval=200, blit=True)
ani.save(filename="cubes.gif", writer=PillowWriter(fps=24))
