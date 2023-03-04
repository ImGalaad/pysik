import numpy as np
from src.memoize import memoize

class Collision:
    def __init__(self, obj1, obj2, normal, penetration):
        self.obj1 = obj1
        self.obj2 = obj2
        self.normal = normal
        self.penetration = penetration
    
    def resolve(self):
        resolve = self.normal * self.penetration

        self.obj1.position += resolve
        self.obj2.position -= resolve

        relative_velocity = self.obj1.velocity - self.obj2.velocity
        velocity_along_normal = np.dot(relative_velocity, self.normal)
        
        if velocity_along_normal > 0:
            return

        e = 0.7

        j = -(1 + e) * velocity_along_normal / (1 / self.obj1.mass + 1 / self.obj2.mass)
        impulse = self.normal * j

        self.obj1.velocity += impulse / self.obj1.mass
        self.obj2.velocity -= impulse / self.obj2.mass

@memoize
def detectCollision(obj1, obj2):
    diff = obj1.position - obj2.position
    distance_squared = np.dot(diff, diff)
    radius_sum_squared = (obj1.radius + obj2.radius) ** 2

    if distance_squared < radius_sum_squared:
        distance = np.sqrt(distance_squared)
        normal = diff / distance
        penetration = obj1.radius + obj2.radius - distance

        return Collision(obj1, obj2, normal, penetration)
    return None
