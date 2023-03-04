import pygame
import random
import numpy as np
import yaml

from src.collision import *
from src.object import *

pygame.init()

with open("config.yml", "r") as file:
    config = yaml.safe_load(file)

TITLE = config["window"]["title"]
WIDTH = config["window"]["width"]
HEIGHT = config["window"]["height"]
BG = config["window"]["background"]
FPS = config["window"]["fps"]
SIZE = 15
NUMBER = 25

dt = 1 / 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()


def main():
    objects = [
        Object(
            random.randint(SIZE, WIDTH - SIZE),
            random.randint(SIZE, HEIGHT - SIZE),
            1,
            SIZE,
            velocity=np.array([random.randint(-5, 5), random.randint(-5, 5)]),
        )
        for i in range(NUMBER)
    ]

    object_positions = np.array([obj.position for obj in objects])
    object_velocities = np.array([obj.velocity for obj in objects])
    object_radii = np.array([obj.radius for obj in objects])

    gravity = np.array(config["forces"]["gravity"])

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        """
        screen.fill(BG)

        for obj in objects:
            obj.gravity(gravity)
            obj.update(dt=delta)

            for other_obj in objects:
                if obj != other_obj:
                    collision = detectCollision(obj, other_obj)
                    if collision:
                        collision.resolve()

            if (
                obj.position[0] - obj.radius < 0
                or obj.position[0] + obj.radius > WIDTH
            ):
                obj.velocity[0] *= -1
            if (
                obj.position[1] - obj.radius < 0
                or obj.position[1] + obj.radius > HEIGHT
            ):
                obj.velocity[1] *= -1

            pygame.draw.circle(
                screen, (255, 255, 255), obj.position.astype(int), obj.radius
            )
        """

        object_velocities += gravity
        object_positions += object_velocities * dt

        colliding_pairs = set()
        for i in range(NUMBER):
            overlaps = (object_radii[i] + object_radii) > np.linalg.norm(
                object_positions[i] - object_positions, axis=1
            )
            colliding_pairs |= set([(i, j) for j in np.nonzero(overlaps)[0] if i < j])

        for i, j in colliding_pairs:
            collision = detectCollision(objects[i], objects[j])
            if collision:
                collision.resolve()

        out_of_bounds = np.logical_or(
            np.logical_or(
                object_positions[:, 0] - object_radii < 0,
                object_positions[:, 0] + object_radii > WIDTH,
            ),
            np.logical_or(
                object_positions[:, 1] - object_radii < 0,
                object_positions[:, 1] + object_radii > HEIGHT,
            ),
        )
        object_velocities[out_of_bounds, 0] *= -1
        object_velocities[out_of_bounds, 1] *= -1

        screen.fill(BG)
        for i, obj in enumerate(objects):
            pygame.draw.circle(
                screen, (255, 255, 255), object_positions[i].astype(int), obj.radius
            )

        pygame.display.update()

        pygame.display.set_caption(str(int(clock.get_fps())))
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
