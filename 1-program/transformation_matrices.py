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

def draw_circle(xc, yc, z, r):
    """Draw a circle centered at (xc, yc) with radius r and color z"""
    x = 0
    y = r
    d = 3 - 2 * r
    while x <= y:
        image_array[xc + x, yc + y] = z
        image_array[xc + y, yc + x] = z
        image_array[xc - y, yc + x] = z
        image_array[xc - x, yc + y] = z
        image_array[xc - x, yc - y] = z
        image_array[xc - y, yc - x] = z
        image_array[xc + y, yc - x] = z
        image_array[xc + x, yc - y] = z
        x += 1
        if d < 0:
            d += 4 * x + 6
        else:
            d += 4 * (x - y) + 10
            y -= 1

def draw_bezier_curve(p0, p1, p2, p3, z):
    """Draw a Bezier curve defined by control points p0, p1, p2, and p3 with color z"""
    for t in np.linspace(0, 1, 1000):
        x = (1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1]
        image_array[int(x), int(y)] = z

def draw_hermite_curve(p0, p1, r0, r1, z):
    """Draw a Hermite curve defined by control points p0, p1 and tangents r0, r1 with color z"""
    for t in np.linspace(0, 1, 1000):
        h00 = 2 * t**3 - 3 * t**2 + 1
        h01 = -2 * t**3 + 3 * t**2
        h10 = t**3 - 2 * t**2 + t
        h11 = t**3 - t**2
        x = h00 * p0[0] + h01 * p1[0] + h10 * r0[0] + h11 * r1[0]
        y = h00 * p0[1] + h01 * p1[1] + h10 * r0[1] + h11 * r1[1]
        image_array[int(x), int(y)] = z


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

def identity_matrix():
    """
    Returns a 4x4 identity matrix.
    """
    return np.eye(4)

def apply_transform(edges, matrix):
    """Apply a transformation matrix to an edge list"""
    for i in range(len(edges)):
        point = np.array(edges[i][:3])
        transformed_point = matrix @ point
        edges[i] = [transformed_point[0], transformed_point[1], transformed_point[2], 1]

def save_image(filename, image):
    """Save the image as a PPM file and convert it to a PNG file"""
    edge_array = np.array(edge_list)
    num_points = edge_array.shape[0]
    for i in range(0, num_points - 1, 2):
        x1, y1, z1, _ = edge_array[i]
        x2, y2, z2, _ = edge_array[i + 1]
        bresenham_line_algorithm(x1, y1, x2, y2, z1)  # draw a line between the two points

    # Save the image as a PPM file
    with open(filename + ".ppm", "wb") as f:
        f.write(b"P6\n")
        f.write(bytes(f"{image_width} {image_height}\n", "ascii"))
        f.write(b"255\n")
        image.tofile(f)

    # Convert the PPM file to a PNG file using ImageMagick
    subprocess.run(["convert", filename + ".ppm", filename + ".png"])

def save_ppm(filename, width, height, edge_list):
    # Create an empty image with the specified width and height
    img = Image.new("RGB", (width, height), "white")
    pixels = img.load()

    # Plot the points from the edge list
    plot_edge_list(edge_list, pixels)

    # Save the image as a PNG file
    img.save(filename, "PNG")


def plot_edge_list(edge_list, pixels):
    # Iterate over every two consecutive points in the edge list and draw a line between them
    for i in range(0, len(edge_list) - 1, 2):
        x0, y0, _, _ = edge_list[i]
        x1, y1, _, _ = edge_list[i + 1]
        bresenham_line(x0, y0, x1, y1, pixels)

# Define the edge list
edge_list = [[50, 50, 0, 1], [450, 50, 0, 1], [450, 450, 0, 1], [50, 450, 0, 1], [50, 50, 0, 1]]

# Define the image dimensions
image_width = 500
image_height = 500

# Initialize the image array with zeros
image_array = np.zeros((image_width, image_height), dtype=np.float32)

# Plot the points from the edge list
edge_array = np.array(edge_list)
num_points = edge_array.shape[0]
for i in range(num_points):
    x, y, z, _ = edge_array[i]
    image_array[x, y] = z

# Save and display the image
save_image("test_image", image_array)
subprocess.run(["display", "test_image.png"])
