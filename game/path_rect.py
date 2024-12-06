import pygame
import math

def generate_path_rects(waypoints, path_width):
    path_rects = []
    for i in range(len(waypoints) - 1):
        start_pos = waypoints[i]
        end_pos = waypoints[i + 1]
        rect = create_rect_between_points(start_pos, end_pos, path_width)
        path_rects.append(rect)
    return path_rects

def create_rect_between_points(start_pos, end_pos, path_width):
    # Calculate the direction vector
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    angle = math.atan2(dy, dx)

    # Calculate the length between points
    length = math.hypot(dx, dy)

    # Create a surface to rotate
    surf = pygame.Surface((length, path_width), pygame.SRCALPHA)
    rect = surf.get_rect(center=((start_pos[0] + end_pos[0]) / 2, (start_pos[1] + end_pos[1]) / 2))

    # Rotate the rectangle
    rotated_surf = pygame.transform.rotate(surf, -math.degrees(angle))
    rotated_rect = rotated_surf.get_rect(center=rect.center)

    return rotated_rect

def generate_path_polygons(waypoints, path_width):
    polygons = []
    half_width = path_width / 2

    for i in range(len(waypoints) - 1):
        start = waypoints[i]
        end = waypoints[i + 1]

        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)

        if length == 0:
            continue  # Avoid division by zero

        # Normalize direction vector
        nx = dx / length
        ny = dy / length

        # Perpendicular vector
        px = -ny
        py = nx

        # Calculate corners of the polygon
        corner1 = (start[0] + px * half_width, start[1] + py * half_width)
        corner2 = (start[0] - px * half_width, start[1] - py * half_width)
        corner3 = (end[0] - px * half_width, end[1] - py * half_width)
        corner4 = (end[0] + px * half_width, end[1] + py * half_width)

        polygons.append([corner1, corner2, corner3, corner4])

    return polygons