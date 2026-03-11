import pygame
import sys
import math
import json

# Configuration
width, height = 800, 600
fps = 60
bgcolor = (20, 20, 20)

G = 60.0

# Initialization
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("N Bodies")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

# import body definitions
with open("bodies.json") as f:
    bodies = json.load(f)

for b in bodies:
    b["trail"] = []
    b["ax"] = 0
    b["ay"] = 0
    b["color"] = tuple(b["color"])

# Zero total momentum (center-of-mass frame)
px = sum(b["m"] * b["vx"] for b in bodies)
py = sum(b["m"] * b["vy"] for b in bodies)
total_mass = sum(b["m"] for b in bodies)

for b in bodies:
    b["vx"] -= px / total_mass
    b["vy"] -= py / total_mass

# Flat array to store states for RK4
state = []
for b in bodies:
    state += [b["x"], b["y"], b["vx"], b["vy"]]

def derivatives(state):
    n = len(bodies)
    ax = [0.0] * n
    ay = [0.0] * n

    for i in range(n):
        for j in range(i + 1, n):
            xi, yi = state[i*4], state[i*4 + 1]
            xj, yj = state[j*4], state[j*4 + 1]

            dx = xj - xi
            dy = yj - yi
            distance = math.hypot(dx, dy)

            if distance == 0:
                continue

            softenting = 20
            force = G * bodies[i]["m"] * bodies[j]["m"] / (distance * distance + softenting * softenting)

            ax[i] += force * (dx / distance) / bodies[i]["m"]
            ay[i] += force * (dy / distance) / bodies[i]["m"]
            ax[j] -= force * (dx / distance) / bodies[j]["m"]
            ay[j] -= force * (dy / distance) / bodies[j]["m"]

    ds = []
    for i in range(n):
        ds += [state[i*4+2], state[i*4+3], ax[i], ay[i]]

    return ds


def rk4_step(state, dt):
    k1 = derivatives(state)
    k2 = derivatives([state[i] + dt / 2 * k1[i] for i in range(len(state))])
    k3 = derivatives([state[i] + dt / 2 * k2[i] for i in range(len(state))])
    k4 = derivatives([state[i] + dt * k3[i] for i in range(len(state))])

    return [
        state[i] + dt / 6 * (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i])
        for i in range(len(state))
    ]

# Main Loop
running = True
while running:
    clock.tick(fps)
    dt = 1/60

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    state = rk4_step(state, dt)

    for i, b in enumerate(bodies):
        b["x"] = state[i*4]
        b["y"] = state[i*4+1]
        b["vx"] = state[i*4+2]
        b["vy"] = state[i*4+3]
        b["trail"].append((b["x"], b["y"]))
        if len(b["trail"]) > 300:
            b["trail"].pop(0)

    # Render
    screen.fill(bgcolor)

    for body in bodies:
        if len(body["trail"]) > 1:
            pygame.draw.lines(screen, body["color"], False, body["trail"], 1)
    for body in bodies:
        pygame.draw.circle(
            screen, body["color"], (int(body["x"]), int(body["y"])), body["r"]
        )

    debug_lines = [f"G: {G}"]

    for idx, b in enumerate(bodies):
        debug_lines += [
            f"x{idx+1}: {b['x']:.1f}",
            f"y{idx+1}: {b['y']:.1f}",
            f"vx{idx+1}: {b['vx']:.1f}",
            f"vy{idx+1}: {b['vy']:.1f}",
            f"m{idx+1}: {b['m']:.1f}",
        ]
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            d = math.hypot(
                bodies[i]["x"] - bodies[j]["x"], bodies[i]["y"] - bodies[j]["y"]
            )
            debug_lines.append(f"Dist({i+1}-{j+1}): {d:.1f}")
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
