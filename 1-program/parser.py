from typing import List, Tuple
from transformation_matrices import *

def parse_script(script: str) -> None:
    edge_matrix = []
    transform_matrix = identity_matrix()

    lines = script.strip().split('\n')
    for i in range(len(lines)):
        parts = lines[i].strip().split()
        if len(parts) > 0:
            cmd = parts[0]
            args = []
            if cmd == 'line' and len(parts) == 7:
                args = list(map(float, parts[1:]))
                add_edge(edge_matrix, *args)
            elif cmd == 'scale' and len(parts) == 4:
                args = list(map(float, parts[1:]))
                scale_matrix = create_dilation_matrix(*args)
                transform_matrix = multiply_matrices(transform_matrix, scale_matrix)
            elif cmd == 'move' and len(parts) == 4:
                args = list(map(float, parts[1:]))
                translation_matrix = create_translation_matrix(*args)
                transform_matrix = multiply_matrices(transform_matrix, translation_matrix)
            elif cmd == 'rotate' and len(parts) == 3:
                axis = parts[1]
                theta = float(parts[2])
                if axis == 'x':
                    rotation_matrix = create_rotation_matrix_x(theta)
                elif axis == 'y':
                    rotation_matrix = create_rotation_matrix_y(theta)
                elif axis == 'z':
                    rotation_matrix = create_rotation_matrix_z(theta)
                transform_matrix = multiply_matrices(transform_matrix, rotation_matrix)
            elif cmd == 'apply' and len(parts) == 1:
                apply_matrix(edge_matrix, transform_matrix)
            elif cmd == 'display' and len(parts) == 1:
                clear_screen()
                draw_lines(edge_matrix)
                display_screen()
            elif cmd == 'save' and len(parts) == 2:
                file_name = parts[1]
                clear_screen()
                draw_lines(edge_matrix)
                save_extension(file_name)
            elif cmd == 'ident' and len(parts) == 1:
                transform_matrix = identity_matrix()
            else:
                raise ValueError(f"Invalid command: {lines[i]}")
