import pygame
import sys
import math

# Configuration
width, height = 800, 600
fps = 60
bgcolor = (20, 20, 20)

G = 60.0

# Initialization
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Three Bodies")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

# Body definitions
bodies = [
    # Star A
    {
        "x": width // 2 - 60,
        "y": height // 2,
        "vx": 45,
        "vy": -45,
        "m": 15000,
        "r": 6,
        "color": (255, 180, 180),
        "ax": 0,
        "ay": 0,
        "trail": []
    },
    # Star B
    {
        "x": width // 2 + 60,
        "y": height // 2,
        "vx": -45,
        "vy": 45,
        "m": 15000,
        "r": 6,
        "color": (180, 180, 255),
        "ax": 0,
        "ay": 0,
        "trail": []
    },
    # Third body (outer orbit)
    {
        "x": width // 2,
        "y": height // 2 - 180,
        "vx": -45,
        "vy": -45,
        "m": 15000,
        "r": 6,
        "color": (180, 255, 180),
        "ax": 0,
        "ay": 0,
        "trail": []
    },
]

# Zero total momentum (center-of-mass frame)
px = sum(b["m"] * b["vx"] for b in bodies)
py = sum(b["m"] * b["vy"] for b in bodies)
total_mass = sum(b["m"] for b in bodies)

for b in bodies:
    b["vx"] -= px / total_mass
    b["vy"] -= py / total_mass

# Main Loop
running = True
while running:
    dt = clock.tick(fps) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Reset accelerations
    for b in bodies:
        b["ax"] = 0
        b["ay"] = 0
    # Physics update
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):

            bi = bodies[i]
            bj = bodies[j]

            dx = bj["x"] - bi["x"]
            dy = bj["y"] - bi["y"]

            distance = math.hypot(dx, dy)

            if distance == 0:
                continue

            ux = dx / distance
            uy = dy / distance

            softenting = 20
            force = (
                G * bi["m"] * bj["m"] / (distance * distance + softenting * softenting)
            )

            Fx = force * ux
            Fy = force * uy

            # Newton's 3rd law (equal & opposite)
            bi["ax"] += Fx / bi["m"]
            bi["ay"] += Fy / bi["m"]

            bj["ax"] -= Fx / bj["m"]
            bj["ay"] -= Fy / bj["m"]

    for b in bodies:
        b["vx"] += b["ax"] * dt
        b["vy"] += b["ay"] * dt

        b["x"] += b["vx"] * dt
        b["y"] += b["vy"] * dt

        b["trail"].append((b["x"],b["y"]))
        if len(b["trail"]) > 300:
            b["trail"].pop(0)

    # Render
    screen.fill(bgcolor)

    for body in bodies:
        if len(body["trail"]) > 1:
            pygame.draw.lines(
                screen,
                body["color"],
                False,
                body["trail"],
                1
            )
    for body in bodies:
        pygame.draw.circle(
            screen, body["color"], (int(body["x"]), int(body["y"])), body["r"]
        )

    b1 = bodies[0]
    b2 = bodies[1]
    b3 = bodies[2]
    d12 = math.hypot(b1["x"] - b2["x"], b1["y"] - b2["y"])
    d13 = math.hypot(b1["x"] - b3["x"], b1["y"] - b3["y"])
    d23 = math.hypot(b2["x"] - b3["x"], b2["y"] - b3["y"])
    debug_lines = [
        f"x1: {b1["x"]:.1f}",
        f"y1: {b1["y"]:.1f}",
        f"x2: {b2["x"]:.1f}",
        f"y2: {b2["y"]:.1f}",
        f"x3: {b3["x"]:.1f}",
        f"y3: {b3["y"]:.1f}",
        f"vx1: {b1["vx"]:.1f}",
        f"vy1: {b1["vy"]:.1f}",
        f"vx2: {b2["vx"]:.1f}",
        f"vy2: {b2["vy"]:.1f}",
        f"vx3: {b3["vx"]:.1f}",
        f"vy3: {b3["vy"]:.1f}",
        f"m1: {b1["m"]:.1f}",
        f"m2: {b2["m"]:.1f}",
        f"m3: {b3["m"]:.1f}",
        f"G: {G}",
        f"Distance(1-2): {d12:.1f}",
        f"Distance(1-3): {d13:.1f}",
        f"Distance(2-3): {d23:.1f}",
    ]

    y_offset = 10
    for line in debug_lines:
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(topleft=(10, y_offset))
        screen.blit(text_surface, text_rect)
        y_offset += text_surface.get_height() + 2

    pygame.display.flip()

# Shutdown
pygame.quit()
sys.exit()
