import numpy as np
from PIL import Image
import subprocess

def bresenham_line_algorithm(x1, y1, x2, y2, z):
    """Bresenham's Line Algorithm"""
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy
    while x1 != x2 or y1 != y2:
        image_array[x1, y1] = z  # draw the pixel on the image
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    image_array[x1, y1] = z  # draw the last pixel on the image

def add_edge(edge_list, x1, y1, z1, x2, y2, z2):
    """Add two points to the edge list"""
    edge_list.append([x1, y1, z1, 1])
    edge_list.append([x2, y2, z2, 1])

def create_translation_matrix(tx, ty, tz):
    """Create a 4x4 translation matrix"""
    return np.array([[1, 0, 0, tx],
                     [0, 1, 0, ty],
                     [0, 0, 1, tz],
                     [0, 0, 0, 1]])

def create_rotation_matrix_x(theta):
    """Create a 4x4 rotation matrix around the x-axis"""
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([[1, 0, 0, 0],
                     [0, cos_t, -sin_t, 0],
                     [0, sin_t, cos_t, 0],
                     [0, 0, 0, 1]])

def create_rotation_matrix_y(theta):
    """Create a 4x4 rotation matrix around the y-axis"""
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([[cos_t, 0, sin_t, 0],
                     [0, 1, 0, 0],
                     [-sin_t, 0, cos_t, 0],
                     [0, 0, 0, 1]])

def create_rotation_matrix_z(theta):
    """Create a 4x4 rotation matrix around the z-axis"""
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    return np.array([[cos_t, -sin_t, 0, 0],
                     [sin_t, cos_t, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]])

def create_dilation_matrix(sx, sy, sz):
    """Create a 4x4 dilation matrix"""
    return np.array([[sx, 0, 0, 0],
                     [0, sy, 0, 0],
                     [0, 0, sz, 0],
                     [0, 0, 0, 1]])

def save_image(filename):
    """Save the image as a PPM file and convert it to a PNG file"""
    image = Image.fromarray(np.uint8(image_array * 255
