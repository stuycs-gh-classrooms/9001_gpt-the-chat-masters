from typing import List, Tuple
from transformation_matrices import *

def parse_script(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    transform = identity_matrix()
    edges = []
    for i in range(len(lines)):
        command = lines[i].strip()
        if command == 'line':
            args = list(map(int, lines[i+1].split()))
            add_edge(edges, args[0], args[1], args[2], args[3], args[4], args[5])
            i += 1
        elif command == 'ident':
            transform = identity_matrix()
        elif command == 'scale':
            args = list(map(float, lines[i+1].split()))
            transform = matrix_mult(transform, create_dilation_matrix(args[0], args[1], args[2]))
            i += 1
        elif command == 'move':
            args = list(map(float, lines[i+1].split()))
            transform = matrix_mult(transform, create_translation_matrix(args[0], args[1], args[2]))
            i += 1
        elif command == 'rotate':
            args = lines[i+1].split()
            if args[0] == 'x':
                transform = matrix_mult(transform, create_rotation_matrix_x(float(args[1])))
            elif args[0] == 'y':
                transform = matrix_mult(transform, create_rotation_matrix_y(float(args[1])))
            elif args[0] == 'z':
                transform = matrix_mult(transform, create_rotation_matrix_z(float(args[1])))
            i += 1
        elif command == 'apply':
            edges = matrix_mult(transform, edges)
        elif command == 'display':
            clear_screen(screen)
            draw_lines(edges, screen, color)
            display(screen)
        elif command == 'save':
            args = lines[i+1].strip()
            clear_screen(screen)
            draw_lines(edges, screen, color)
            save_ppm(screen, args)
            i += 1
    return edges
