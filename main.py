import pygame
import sys

# -----------------------------
# Configuration
# -----------------------------
width, height = 800, 600
fps = 60
bgcolor = (25, 25, 25)
circle_color = (200, 255, 255)

GRAVITY = 1000 #pixels per second squared

# -----------------------------
# Initialization
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Physics Engine")
clock = pygame.time.Clock()

# -----------------------------
# Physics state
# -----------------------------
x = width // 2
y = 100          # start near the top
vy = 0           # vertical velocity (px/s)
radius = 30

# -----------------------------
# Main Loop
# -----------------------------
running = True
while running:
    # --- Timing ---
    dt = clock.tick(fps) / 1000.0  # delta time in seconds

    # --- Event handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Physics update ---
    vy += GRAVITY * dt      # v = v + a·dt
    y += vy * dt            # y = y + v·dt

    # --- Render ---
    screen.fill(bgcolor)

    pygame.draw.circle(
        screen,
        circle_color,
        (int(x), int(y)),
        radius
    )

    if y - radius > height:
        y = 100
        vy = 0


    pygame.display.flip()

    # --- Timing ---
    clock.tick(fps)

# -----------------------------
# Shutdown
# -----------------------------
pygame.quit()
sys.exit()
