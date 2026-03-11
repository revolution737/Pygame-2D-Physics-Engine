# N-Body Physics Engine

A gravitational N-body simulator built in Python with Pygame. This project started as a general 2D physics engine simulating projectile motion and restitution, then progressively evolved into a full gravitational simulator — first two bodies, then three, and finally an arbitrary number of bodies with configurable initial conditions and real-time energy monitoring.

---

## Evolution of the Project

**Projectile motion** — the starting point. Basic kinematics: velocity, acceleration, gravity, and coefficient of restitution for bouncing. The goal was to get comfortable simulating physical systems from first principles.

**Two-body** — introduced gravitational attraction between two masses using Newton's law of gravitation. Clean and predictable — two bodies always produce a stable closed orbit with an exact analytical solution.

**Three-body** — the moment things got interesting. Adding a third body means there is no closed-form solution. The system becomes chaotic: trajectories are deterministic but extremely sensitive to initial conditions. This is the classical three-body problem.

**N-body** — generalized the simulation so any number of bodies can be added by editing a single JSON file. The physics loop already scaled naturally; the main work was making the codebase clean enough to support it.

---

## What This Project Actually Does

- Simulates gravitational interactions between N bodies in 2D
- Runs two integrators side by side: **Euler** and **Runge-Kutta 4 (RK4)**
- Plots total system energy in real time using matplotlib
- Bodies are configured externally via `bodies.json` — no code changes needed to add or modify bodies
- Uses a fixed timestep (`dt = 1/60`) for deterministic, reproducible results

---

## Euler vs RK4

The core technical question this project explores is: does integrator choice matter?

**Euler integration** computes acceleration once per frame and steps forward blindly. It assumes forces are constant across the entire timestep, which they are not. In a chaotic gravitational system, this error accumulates.

**Runge-Kutta 4** samples the derivative four times per timestep — at the start, twice at the midpoint, and once at the end — then blends them with weights `1, 2, 2, 1`. This gives fourth-order accuracy, meaning error scales with `dt^4` instead of `dt^1`.

The difference is visible in the energy graphs below.

### Energy Conservation Comparison (softening = 5)

<img width="791" height="563" alt="image" src="https://github.com/user-attachments/assets/486c63e1-ecb3-44a2-b308-f6070266b776" />

<img width="640" height="480" alt="rk4" src="https://github.com/user-attachments/assets/15cab16e-8038-412a-852a-852cd388b2e4" />

<img width="640" height="480" alt="euler" src="https://github.com/user-attachments/assets/d656ea79-6513-4794-814b-f5a9e959231c" />

| RK4 | Euler |
|-----|-------|
| Flat baseline until a genuine close encounter at t≈6, then stable again |
| Oscillating baseline from the start, energy artificially injected on every close encounter, catastrophic ejection at t≈14 |

Both systems eventually eject a body under these conditions — but RK4's ejection is a real physical event caused by an extreme close encounter. Euler's ejection is caused by accumulated numerical error artificially pumping energy into the system on every interaction until the system destabilizes.

---

## The Three-Body Problem

A common misconception is that chaotic means random. It does not.

The three-body problem is **deterministic but unpredictable**. Given identical initial conditions, the simulation produces identical results every time. The chaos refers to sensitivity to initial conditions — a position difference of `0.001` pixels at t=0 produces a completely different trajectory by t=100. This is why long-term prediction of three-body systems is practically impossible, even though the underlying physics is exact.

This also means the variation in simulation behavior is not a bug. It is the physics working correctly.

---

## Key Implementation Details

**Fixed timestep** — `dt = 1/60` is hardcoded rather than using the real elapsed frame time. Variable `dt` makes simulations feel smooth on different hardware but introduces non-determinism — the same initial conditions produce different results depending on CPU load. Fixed `dt` ensures reproducibility.

**Softening** — the gravitational force formula includes a softening term `ε` in the denominator: `F = G * m1 * m2 / (r² + ε²)`. Without it, force approaches infinity as two bodies get arbitrarily close, causing numerical explosion. Softening puts a floor on the denominator, approximating the fact that real extended bodies would collide and merge rather than pass through each other as point masses.

**Flat state vector** — RK4 requires evaluating the system at hypothetical mid-step positions without mutating the actual body data. The physics state is stored as a flat list `[x0, y0, vx0, vy0, x1, y1, vx1, vy1, ...]` that can be passed into the derivative function and operated on with list comprehensions.

**External configuration** — body definitions live in `bodies.json`. Mass, position, velocity, radius, and color are all configurable. The simulation scales to any number of bodies automatically.

---

## Project Structure

```
N-Body-Physics-Engine/
├── engine/
│   ├── nbody-rk4.py       # N-body simulation with RK4 integrator
│   ├── nbody-euler.py     # N-body simulation with Euler integrator
├── bodies.json            # Body configuration file
└── README.md
```

---

## Running the Simulation

Install dependencies:
```
pip install pygame matplotlib
```

Edit `bodies.json` to define your bodies, then run either:
```
cd engine
python nbody-rk4.py
python nbody-euler.py
```

Both simulations load from the same `bodies.json` so comparisons are exact.

---

## bodies.json Format

```json
[
    {
        "x": 340, "y": 300,
        "vx": 45, "vy": -45,
        "m": 15000, "r": 6,
        "color": [255, 180, 180]
    }
]
```

Add as many body objects as you want. The simulation handles the rest.

---

## Dependencies

- Python 3.x
- pygame
- matplotlib
