import pygame
import numpy as np
from .physics import normalise_vector, magnitude_vector, distance_between_points
from .pellet import Pellet

max_accelleration = 3
FRICTION = 0.2
MAX_SPEED = 10
MIN_SPEED = 0.05


class Creature(pygame.sprite.Sprite):
    def __init__(self, initial_location, initial_velocity=[0, 0], radius=10):
        super().__init__()
        self.coords = np.array(initial_location).astype(float)
        self.velocity = np.array(initial_velocity).astype(float)
        self.last_coords = self.coords - self.velocity
        self.max_accelleration = max_accelleration
        self.accelleration = np.array([0.0, 0.0])
        self.colour = (200, 20, 20)
        self.rect = pygame.Rect(*((0, 0) + (2 * radius, 2 * radius)))
        self.change_rect_center(self.coords)
        self.arrive_distance = 5.0
        self.eaten = False

    def update(self, screen, objects):
        objects = [thing for thing in objects if thing != self]
        if len(objects) > 0:
            closest = self.closest_object(objects)
            target_position = (
                closest.coords
            )  # np.array(pygame.mouse.get_pos()).astype(float)
        else:
            target_position = np.array([20, 20])
        vector = self.seek(target_position)
        self.set_accelleration(vector)
        self.move()
        if self.coords[0] < 5:
            self.coords[0] = 5
        if self.coords[1] < 5:
            self.coords[1] = 5
        if self.coords[0] > 635:
            self.coords[0] = 635
        if self.coords[1] > 635:
            self.coords[1] = 635
        self.draw(self.coords, screen)

    def apply_friction(self, velocity):
        opposite_vector = -normalise_vector(velocity)
        magnitude = magnitude_vector(velocity)
        friction_force = magnitude * FRICTION
        friction = opposite_vector * friction_force
        return velocity + friction

    def apply_max_speed(self, velocity):
        speed = magnitude_vector(velocity)
        if speed > MAX_SPEED:
            vector = normalise_vector(velocity)
            velocity = vector * MAX_SPEED
        return velocity

    def apply_min_speed(self, velocity):
        speed = magnitude_vector(velocity)
        if speed < MIN_SPEED:
            velocity = np.array((0, 0))
        return velocity

    def recalculate_velocity(self):
        velocity = self.coords - self.last_coords
        velocity += self.accelleration
        velocity = self.apply_friction(velocity)
        velocity = self.apply_max_speed(velocity)
        velocity = self.apply_min_speed(velocity)
        self.velocity = velocity

    def set_accelleration(self, goal_vector):
        self.accelleration = goal_vector * self.max_accelleration

    def move(self):
        self.recalculate_velocity()
        self.last_coords = self.coords
        self.coords = self.velocity + self.coords

    def change_rect_center(self, coords):
        self.rect.centerx = int(coords[0].round())
        self.rect.centery = int(coords[1].round())

    def draw(self, coords, screen):
        self.change_rect_center(coords)
        pygame.draw.ellipse(screen, self.colour, self.rect)

    def calculate_vector_to_target(
        self, current_position, current_velocity, target_position
    ):
        anticipated_position = current_position + current_velocity
        vector = normalise_vector(target_position - anticipated_position)
        return vector

    def arrive_factor(self, current_position, current_velocity, target_position):
        anticipated_position = current_position + current_velocity
        current_distance_to_target = distance_between_points(
            anticipated_position, target_position
        )
        if current_distance_to_target < self.arrive_distance:
            return current_distance_to_target / self.arrive_distance
        else:
            return 1.0

    def stop(self, position, velocity):
        speed = magnitude_vector(velocity)
        return -normalise_vector(velocity) * speed

    def seek(self, target_position):
        vector_to_target = self.calculate_vector_to_target(
            self.coords, self.velocity, target_position
        )
        arrive_factor = self.arrive_factor(self.coords, self.velocity, target_position)
        return normalise_vector(vector_to_target) * arrive_factor

    def interact(self, thing):
        if thing.__class__ == Pellet:
            thing.eaten = True

    def closest_object(self, objects):
        distances = np.array(
            [distance_between_points(self.coords, thing.coords) for thing in objects]
        )
        idx = np.argmin(distances)
        return objects[idx]
