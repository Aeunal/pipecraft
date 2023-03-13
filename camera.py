import math
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *

PERSPECTIVE = 60

class Camera:
    def __init__(self):
        # Initialize camera rotation and position variables
        self.camera_rotation_x = 0.0
        self.camera_rotation_y = 0.0
        self.camera_position_x = 0.0
        self.camera_position_y = 1.0 # Eye level
        self.camera_position_z = 0.0
        # Initialize gravity and vertical velocity variables
        self.gravity = -0.05
        self.vertical_velocity = 0.0
        self.ground_level = 0.0  # Adjust ground level to match eye level

        # Set the initial position of the mouse to the screen center
        pygame.mouse.set_pos(pygame.display.get_surface().get_width() // 2, pygame.display.get_surface().get_height() // 2)
        # Capture the mouse - enters a virtual input mode
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_dx, mouse_dy = event.rel
            self.camera_rotation_x += mouse_dy * 0.1
            self.camera_rotation_y += mouse_dx * 0.1

    def handle_keys(self, keys):
        move_speed = 0.5

        # Check MOVE
        if keys[pygame.K_w]:
            self.camera_position_x += move_speed * math.sin(math.radians(self.camera_rotation_y))
            self.camera_position_z += move_speed * math.cos(math.radians(self.camera_rotation_y))
        if keys[pygame.K_s]:
            self.camera_position_x -= move_speed * math.sin(math.radians(self.camera_rotation_y))
            self.camera_position_z -= move_speed * math.cos(math.radians(self.camera_rotation_y))
        if keys[pygame.K_a]:
            self.camera_position_x -= move_speed * math.sin(math.radians(self.camera_rotation_y + 90))
            self.camera_position_z -= move_speed * math.cos(math.radians(self.camera_rotation_y + 90))
        if keys[pygame.K_d]:
            self.camera_position_x -= move_speed * math.sin(math.radians(self.camera_rotation_y - 90))
            self.camera_position_z -= move_speed * math.cos(math.radians(self.camera_rotation_y - 90))
        
        # Check JUMP
        if keys[pygame.K_SPACE] and self.camera_position_y == self.ground_level:
            self.vertical_velocity = 0.8

    def update(self):
        # Update the camera's vertical position based on gravity and vertical velocity
        self.camera_position_y += self.vertical_velocity
        self.vertical_velocity += self.gravity

        # Check for collision with the ground and stop the camera from going below it
        if self.camera_position_y < self.ground_level:
            self.camera_position_y = self.ground_level
            self.vertical_velocity = 0.0

        # Apply the camera rotation and translation
        glLoadIdentity()
        gluPerspective(PERSPECTIVE, (pygame.display.get_surface().get_width() / pygame.display.get_surface().get_height()), 0.1, 100.0)
        glRotatef(self.camera_rotation_x, 1, 0, 0)
        glRotatef(self.camera_rotation_y, 0, 1, 0)
        glTranslatef(-self.camera_position_x, -self.camera_position_y, self.camera_position_z - 40.0)
