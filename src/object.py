import numpy as np


class Object:
    def __init__(
        self, x: int, y: int, mass: float, radius: int, velocity: np.array = np.zeros(2)
    ):
        self.radius = radius
        self.position = np.array([x, y], dtype=float)
        self.mass = mass
        self.velocity = np.array(velocity, dtype=float)
        self.acceleration = np.zeros(2, dtype=float)
        self.force = np.zeros(2, dtype=float)

    def update_position(self, dt):
        self.position += self.velocity * dt + 0.5 * self.acceleration * dt**2

    def update_velocity(self, dt):
        self.velocity += self.acceleration * dt

    def gravity(self, gravity):
        self.force += self.mass * gravity

    def apply_force(self, force):
        self.force += force

    def update(self, dt):
        self.acceleration = self.force / self.mass
        self.update_position(dt)
        self.update_velocity(dt)
        self.force = np.zeros(2, dtype=float)
