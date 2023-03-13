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
    
    FULLSCREEN_MODE = True
    if FULLSCREEN_MODE:
        # Get the screen size
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        display = (screen_width, screen_height)
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL | pygame.FULLSCREEN)
    else:
        display = (800, 600)
        pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    # Get the screen center coordinates
    screen_center = (display[0] // 2, display[1] // 2)

    gluPerspective(60, (display[0] / display[1]), 0.1, 100.0)
    glTranslatef(0.0, 0.0, -40.0)
    
    # Enable back-face culling
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)

    # Initialize camera rotation and position variables
    camera_rotation_x = 0.0
    camera_rotation_y = 0.0
    camera_position_x = 0.0
    camera_position_y = 1.0 # Eye level
    camera_position_z = 0.0

    # Initialize gravity and vertical velocity variables
    gravity = -0.05
    vertical_velocity = 0.0

    # Set the initial position of the mouse to the screen center
    pygame.mouse.set_pos(screen_center)

    # Capture the mouse - enters a virtual input mode
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Load the stone texture
    stone_texture = load_texture("./mnt/data/minecraft_stone_texture.webp")

    glEnable(GL_TEXTURE_2D)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                mouse_dx, mouse_dy = event.rel
                camera_rotation_x += mouse_dy * 0.1
                camera_rotation_y += mouse_dx * 0.1

        
        # Add key event handling in the event loop
        keys = pygame.key.get_pressed()
        
        # Check if ESC key is pressed
        if keys[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        move_speed = 0.5

        if keys[pygame.K_w]:
            camera_position_x += move_speed * math.sin(math.radians(camera_rotation_y))
            camera_position_z += move_speed * math.cos(math.radians(camera_rotation_y))
        if keys[pygame.K_s]:
            camera_position_x -= move_speed * math.sin(math.radians(camera_rotation_y))
            camera_position_z -= move_speed * math.cos(math.radians(camera_rotation_y))
        if keys[pygame.K_a]:
            camera_position_x -= move_speed * math.sin(math.radians(camera_rotation_y + 90))
            camera_position_z -= move_speed * math.cos(math.radians(camera_rotation_y + 90))
        if keys[pygame.K_d]:
            camera_position_x -= move_speed * math.sin(math.radians(camera_rotation_y - 90))
            camera_position_z -= move_speed * math.cos(math.radians(camera_rotation_y - 90))
        # Check if SPACE key is pressed
        if keys[pygame.K_SPACE] and camera_position_y == ground_level:
            vertical_velocity = 0.8

        # Update the camera's vertical position based on gravity and vertical velocity
        camera_position_y += vertical_velocity
        vertical_velocity += gravity

        # Check for collision with the ground and stop the camera from going below it
        ground_level = 0.0 # Adjust ground level to match eye level
        if camera_position_y < ground_level:
            camera_position_y = ground_level
            vertical_velocity = 0.0


        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Apply the camera rotation
        glLoadIdentity()
        gluPerspective(45, (display[0] / display[1]), 0.1, 100.0)
        glRotatef(camera_rotation_x, 1, 0, 0)
        glRotatef(camera_rotation_y, 0, 1, 0)
        glTranslatef(-camera_position_x, -camera_position_y, camera_position_z - 40.0)


        # Update the camera translation in the main loop
        #glTranslatef(camera_position_x, camera_position_y, camera_position_z - 40.0)

        for x in range(world_size):
            for y in range(world_size):
                for z in range(world_size):
                    if world[x][y][z] == "stone":
                        draw_cube(x * 2, y * 2, z * 2, stone_texture)

        pygame.display.flip()
        pygame.time.wait(10)

display_world()