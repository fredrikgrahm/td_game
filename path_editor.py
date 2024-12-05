import pygame
import json

def main():
    pygame.init()
    WIDTH, HEIGHT = 800, 600  # Use your game's width and height
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Path Editor")

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    font = pygame.font.SysFont('Arial', 24)

    waypoints = []
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    pos = pygame.mouse.get_pos()
                    waypoints.append(pos)

        # Draw waypoints and paths
        for i, point in enumerate(waypoints):
            pygame.draw.circle(screen, RED, point, 5)
            if i > 0:
                pygame.draw.line(screen, BLACK, waypoints[i - 1], point, 2)

        # Instructions
        instructions = [
            "Left-click to add waypoints",
            "Press 'S' to save waypoints",
            "Press 'C' to clear waypoints",
            "Close the window when done"
        ]
        for i, text in enumerate(instructions):
            msg = font.render(text, True, BLACK)
            screen.blit(msg, (10, 10 + i * 30))

        pygame.display.flip()
        clock.tick(60)

        # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            # Save waypoints to file
            with open('waypoints.json', 'w') as f:
                json.dump(waypoints, f)
            print("Waypoints saved to 'waypoints.json'")
            pygame.time.wait(200)  # Delay to prevent multiple saves
        elif keys[pygame.K_c]:
            waypoints.clear()
            print("Waypoints cleared")
            pygame.time.wait(200)  # Delay to prevent multiple clears

    pygame.quit()

if __name__ == "__main__":
    main()