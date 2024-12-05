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