import numpy as np
from PIL import Image
from math import floor

# Define canvas size
canvas_width = 500
canvas_height = 500

# Create canvas with black background
canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

# Define Bresenham's line algorithm
def bresenham_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0
    D = 2*dy - dx
    y = 0
    for x in range(dx + 1):
        yield x1 + x*xx + y*yx, y1 + x*xy + y*yy
        if D >= 0:
            y += 1
            D -= 2*dx
        D += 2*dy

# Define edge list
edge_list = []

# Define functions for creating matrices
def translation_matrix(tx, ty, tz):
    return np.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def rotation_matrix_x(theta):
    return np.array([
        [1, 0, 0, 0],
        [0, np.cos(theta), -np.sin(theta), 0],
        [0, np.sin(theta), np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(theta):
    return np.array([
        [np.cos(theta), 0, np.sin(theta), 0],
        [0, 1, 0, 0],
        [-np.sin(theta), 0, np.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotation_matrix_z(theta):
    return np.array([
        [np.cos(theta), -np.sin(theta), 0, 0],
        [np.sin(theta), np.cos(theta), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def dilation_matrix(sx, sy, sz):
    return np.array([
        [sx, 0, 0, 0],
        [0, sy, 0, 0],
        [0, 0, sz, 0],
        [0, 0, 0, 1]
    ])

# Define function for saving PPM files as PNGs
def save_ppm_as_png(filename, ppm_data):
    img = Image.fromarray(ppm_data, mode='RGB')
    img.save(filename)

# Define function for displaying images using ImageMagick
def display_image(filename):
    from subprocess import run
    run(['display', filename])

# Define function for drawing circles
def draw_circle(center_x, center_y, radius, color):
    for x,
