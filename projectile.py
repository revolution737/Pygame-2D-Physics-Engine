import pygame
import sys

# -----------------------------
# Configuration
# -----------------------------
width, height = 800, 600
fps = 60
bgcolor = (25, 25, 25)
circle_color = (200, 255, 255)
floor_color = (200, 200, 200)

gravity = 1000 #pixels per second squared
restitution = 0.8

# -----------------------------
# Initialization
# -----------------------------
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Physics Engine")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 24)

# -----------------------------
# Physics state
# -----------------------------
x = 100
y = 300     
vx = 100
vy = -500          
radius = 30

floor_y = height - 100

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
    vy += gravity * dt      # v = v + a·dt
    y += vy * dt            # y = y + v·dt
    x += vx * dt
     # Floor collision
    if y + radius >= floor_y:
        y = floor_y - radius
        vy = -vy * restitution

        # stop tiny jitter
        if abs(vy) < 5:
            vy = 0

    # --- Render ---
    screen.fill(bgcolor)

     # Draw floor
    pygame.draw.line(
        screen,
        floor_color,
        (0, floor_y),
        (width, floor_y),
        2
    )

    pygame.draw.circle(
        screen,
        circle_color,
        (int(x), int(y)),
        radius
    )

    # if vy == 0:
    #     y = 100

    # --- Debug text ---
    debug_lines = [
    f"x: {x:.1f}",
    f"y:{y:.1f}",
    f"vx: {vx:.1f}",
    f"vy: {vy:.1f}",
    f"g: {gravity}",
    f"restitution: {restitution}"
]

    y_offset = 10
    for line in debug_lines:
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topright=(width - 10, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += text_surface.get_height() + 2

    pygame.display.flip()

    # --- Timing ---
    clock.tick(fps)

# -----------------------------
# Shutdown
# -----------------------------
pygame.quit()
sys.exit()
