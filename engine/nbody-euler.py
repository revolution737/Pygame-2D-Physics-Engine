import pygame
import sys
import math
import json
import matplotlib.pyplot as plt
import time

start_time = time.time()
time_limit = 60

plt.ion()
fig, ax = plt.subplots()
energy_data = []
time_data = []
t = 0

# Configuration
width, height = 800, 600
fps = 60
bgcolor = (20, 20, 20)

G = 60.0

# Initialization
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("N Bodies by Euler Integration")
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


def total_energy(state, bodies):
    ke = 0
    for i in range(len(bodies)):
        vx, vy = state[i * 4 + 2], state[i * 4 + 3]
        ke += 0.5 * bodies[i]["m"] * (vx**2 + vy**2)

    pe = 0
    for i in range(len(bodies)):
        for j in range(i + 1, len(bodies)):
            dx = state[j * 4] - state[i * 4]
            dy = state[j * 4 + 1] - state[i * 4 + 1]
            dist = math.hypot(dx, dy)
            if dist == 0:
                continue
            pe -= G * bodies[i]["m"] * bodies[j]["m"] / dist

    return ke + pe


# Main Loop
running = True
while running:
    if time.time() - start_time > time_limit:
        running = False
    clock.tick(fps)
    dt = 1 / 60

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

            softenting = 5
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

        b["trail"].append((b["x"], b["y"]))
        if len(b["trail"]) > 300:
            b["trail"].pop(0)

    # Build state from bodies for energy calculation
    state = []
    for b in bodies:
        state += [b["x"], b["y"], b["vx"], b["vy"]]

    t += dt
    energy_data.append(total_energy(state, bodies))
    time_data.append(t)

    if len(time_data) % 60 == 0:
        ax.cla()
        ax.plot(time_data, energy_data)
        ax.set_title("Total Energy - Euler")
        ax.set_xlabel("Time")
        ax.set_ylabel("Energy")
        plt.pause(0.001)

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
plt.ioff()
plt.show()
sys.exit()
