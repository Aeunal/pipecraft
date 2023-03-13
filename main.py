import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Initialize the dimensions of the world
world_size = 16
height = 8

# Create the world
world = [[[None] * world_size for _ in range(world_size)] for _ in range(world_size)]

# Fill the lower part of the world with stone blocks
for x in range(world_size):
    for y in range(world_size):
        for z in range(height):
            world[x][y][z] = "stone"

def load_texture(filename):
    texture_surface = pygame.image.load(filename)
    texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
    width, height = texture_surface.get_size()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

    return texture_id

def draw_cube(x, y, z, texture_id):
    vertices = [
        [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1],
        [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1]
    ]
    
    faces = [
        (4, 7, 3, 0), (3, 2, 1, 0), (4, 5, 6, 7),
        (6, 5, 1, 2), (7, 6, 2, 3), (0, 1, 5, 4)
    ]
    
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glBegin(GL_QUADS)
    for face in faces:
        glTexCoord2f(0, 0); glVertex3f(vertices[face[0]][0] + x, vertices[face[0]][1] + y, vertices[face[0]][2] + z)
        glTexCoord2f(0, 1); glVertex3f(vertices[face[1]][0] + x, vertices[face[1]][1] + y, vertices[face[1]][2] + z)
        glTexCoord2f(1, 1); glVertex3f(vertices[face[2]][0] + x, vertices[face[2]][1] + y, vertices[face[2]][2] + z)
        glTexCoord2f(1, 0); glVertex3f(vertices[face[3]][0] + x, vertices[face[3]][1] + y, vertices[face[3]][2] + z)
    glEnd()



def display_world():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -40.0)
    
    # Enable back-face culling
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Initialize camera rotation variables
    camera_rotation_x = 0.0
    camera_rotation_y = 0.0
    camera_direction_x = 0.0
    camera_direction_y = 0.0
    camera_direction_z = -1.0
    camera_up_x = 0.0
    camera_up_y = 1.0
    camera_up_z = 0.0

    # Initialize camera position variables
    camera_position_x = 0.0
    camera_position_y = 0.0
    camera_position_z = 0.0

    # Initialize gravity and vertical velocity variables
    gravity = -0.05
    vertical_velocity = 0.0

    # Set the initial position of the mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Load the stone texture
    stone_texture = load_texture("./mnt/data/minecraft_stone_texture.webp")

    glEnable(GL_TEXTURE_2D)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Add key event handling in the event loop
        keys = pygame.key.get_pressed()
        move_speed = 0.5

        if keys[pygame.K_s]:
            camera_position_x -= move_speed * math.sin(math.radians(camera_rotation_y))
            camera_position_z -= move_speed * math.cos(math.radians(camera_rotation_y))
        if keys[pygame.K_w]:
            camera_position_x += move_speed * math.sin(math.radians(camera_rotation_y))
            camera_position_z += move_speed * math.cos(math.radians(camera_rotation_y))
        if keys[pygame.K_a]:
            camera_position_x -= move_speed * math.sin(math.radians(camera_rotation_y - 90))
            camera_position_z -= move_speed * math.cos(math.radians(camera_rotation_y - 90))
        if keys[pygame.K_d]:
            camera_position_x -= move_speed * math.sin(math.radians(camera_rotation_y + 90))
            camera_position_z -= move_speed * math.cos(math.radians(camera_rotation_y + 90))

        # Get the current position of the mouse
        new_mouse_x, new_mouse_y = pygame.mouse.get_pos()
        
        # Calculate the difference between the current and previous mouse positions
        mouse_dx = new_mouse_x - mouse_x
        mouse_dy = new_mouse_y - mouse_y

        # Update the camera rotation based on the mouse movement
        camera_rotation_x -= mouse_dy * 0.1
        camera_rotation_y += mouse_dx * 0.1
        
        # Update the camera's direction based on the rotation angles in the main loop
        camera_direction_x = math.sin(math.radians(camera_rotation_y)) * math.cos(math.radians(camera_rotation_x))
        camera_direction_y = math.sin(math.radians(camera_rotation_x))
        camera_direction_z = -math.cos(math.radians(camera_rotation_y)) * math.cos(math.radians(camera_rotation_x))
        
        # Set the new mouse position as the current position for the next frame
        mouse_x, mouse_y = new_mouse_x, new_mouse_y

        # Update the camera's vertical position based on gravity and vertical velocity
        camera_position_y += vertical_velocity
        vertical_velocity += gravity

        # Check for collision with the ground and stop the camera from going below it
        ground_level = 0.0
        if camera_position_y < ground_level:
            camera_position_y = ground_level
            vertical_velocity = 0.0


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Apply the camera rotation
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
        gluLookAt(
            camera_position_x, camera_position_y, camera_position_z,
            camera_position_x + camera_direction_x, camera_position_y + camera_direction_y, camera_position_z + camera_direction_z,
            camera_up_x, camera_up_y, camera_up_z
        )

        # Update the camera translation in the main loop
        glTranslatef(camera_position_x, camera_position_y, camera_position_z - 40.0)

        for x in range(world_size):
            for y in range(world_size):
                for z in range(world_size):
                    if world[x][y][z] == "stone":
                        draw_cube(x * 2, y * 2, z * 2, stone_texture)

        pygame.display.flip()
        pygame.time.wait(10)

display_world()