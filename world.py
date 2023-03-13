from OpenGL.GL import *
from texture import load_texture

class World:
    def __init__(self):
        # Initialize the dimensions of the world
        self.world_size = 16
        self.height = 8

        # Create the world
        self.world = [[[None] * self.world_size for _ in range(self.world_size)] for _ in range(self.world_size)]

        # Fill the lower part of the world with stone blocks
        for x in range(self.world_size):
            for y in range(self.world_size):
                for z in range(self.height):
                    self.world[x][y][z] = "stone"

        # Load the stone texture
        self.stone_texture = load_texture("./mnt/data/minecraft_stone_texture.webp")
        
        glEnable(GL_TEXTURE_2D)
        # Enable back-face culling
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        for x in range(self.world_size):
            for y in range(self.world_size):
                for z in range(self.world_size):
                    if self.world[x][y][z] == "stone":
                        self.draw_cube(x * 2, y * 2, z * 2, self.stone_texture)

    def draw_cube(self, x, y, z, texture_id):
        # ... code to draw a cube with the given texture ...
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