from OpenGL.GL import *
from texture import Texture
import pygame

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
        self.stone_texture_raw = Texture("./mnt/data/minecraft_stone_texture.webp")
        self.stone_texture_tp  = Texture("./mnt/data/minecraft_stone_texture_transparent.png")
        self.stone_texture = self.stone_texture_raw.texture

        glEnable(GL_TEXTURE_2D)
        # Enable back-face culling
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        # Enable depth testing
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        # Enable blending and set blending function
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def handle_keys(self, keys):
        if keys[pygame.K_p]:
            if self.stone_texture_raw.flag:
                self.stone_texture_raw.flag = False
                self.stone_texture = self.stone_texture_tp.texture
            
            elif self.stone_texture_tp.flag:
                self.stone_texture_tp.flag = False
                self.stone_texture = self.stone_texture_raw.texture
        
    def draw(self, camera):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Set the view distance limit
        view_distance = 20.0
        near_plane = 0.1
        far_plane = near_plane + view_distance

        # Extract the frustum with custom near and far planes
        frustum = self.extract_frustum(near_plane, far_plane)
        
        if self.stone_texture_tp.flag:
            glDepthMask(GL_FALSE)
        
        for x in range(self.world_size):
            for y in range(self.world_size):
                for z in range(self.world_size):
                    if self.world[x][y][z] == "stone":
                        cube_position = (x * 2, y * 2, z * 2)
                        if self.cube_in_frustum(*cube_position, 2, frustum):
                            if not self.is_cube_occluded(x, y, z):
                                if self.is_cube_within_distance(cube_position, camera, view_distance):
                                    self.draw_cube(*cube_position, self.stone_texture)
        
        if self.stone_texture_tp.flag:
            glDepthMask(GL_TRUE)

    def is_cube_within_distance(self, cube_position, camera, view_distance):
        camera_position = (camera.camera_position_x, camera.camera_position_y, camera.camera_position_z)
        dx = cube_position[0] - camera_position[0]
        dy = cube_position[1] - camera_position[1]
        dz = cube_position[2] - camera_position[2]
        distance = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
        return distance <= view_distance

    def is_cube_occluded(self, x, y, z):
        # Check if the cube is surrounded by other cubes on all six sides
        if (x > 0 and self.world[x - 1][y][z] == "stone" and
            x < self.world_size - 1 and self.world[x + 1][y][z] == "stone" and
            y > 0 and self.world[x][y - 1][z] == "stone" and
            y < self.world_size - 1 and self.world[x][y + 1][z] == "stone" and
            z > 0 and self.world[x][y][z - 1] == "stone" and
            z < self.height - 1 and self.world[x][y][z + 1] == "stone"):
            return True
        return False

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


    # TODO: make its own file
    def extract_frustum(self, near_plane, far_plane):
        # Extract the frustum planes from the current modelview and projection matrices
        frustum = [0.0] * 24
        proj = (GLdouble * 16)()
        modl = (GLdouble * 16)()
        clip = (GLdouble * 16)()
        glGetDoublev(GL_PROJECTION_MATRIX, proj)
        glGetDoublev(GL_MODELVIEW_MATRIX, modl)

        # Calculate the custom near and far planes
        # ratio = (proj[10] - 1) / (proj[10] + 1)
        # old_near = (proj[14] * ratio) / (ratio - 1)
        # old_far = old_near * (ratio + 1) / (1 - ratio)
        # new_proj14 = (2 * old_near * old_far) / (old_far - near_plane)
        # new_proj10 = -(far_plane + near_plane) / (far_plane - near_plane)

        # Modify the projection matrix with custom near and far planes
        # proj = list(proj)
        # proj[10] = new_proj10
        # proj[14] = new_proj14
        # proj = (GLdouble * 16)(*proj)

        clip[0] = modl[0] * proj[0] + modl[1] * proj[4] + modl[2] * proj[8] + modl[3] * proj[12]
        clip[1] = modl[0] * proj[1] + modl[1] * proj[5] + modl[2] * proj[9] + modl[3] * proj[13]
        clip[2] = modl[0] * proj[2] + modl[1] * proj[6] + modl[2] * proj[10] + modl[3] * proj[14]
        clip[3] = modl[0] * proj[3] + modl[1] * proj[7] + modl[2] * proj[11] + modl[3] * proj[15]

        clip[4] = modl[4] * proj[0] + modl[5] * proj[4] + modl[6] * proj[8] + modl[7] * proj[12]
        clip[5] = modl[4] * proj[1] + modl[5] * proj[5] + modl[6] * proj[9] + modl[7] * proj[13]
        clip[6] = modl[4] * proj[2] + modl[5] * proj[6] + modl[6] * proj[10] + modl[7] * proj[14]
        clip[7] = modl[4] * proj[3] + modl[5] * proj[7] + modl[6] * proj[11] + modl[7] * proj[15]

        clip[8] = modl[8] * proj[0] + modl[9] * proj[4] + modl[10] * proj[8] + modl[11] * proj[12]
        clip[9] = modl[8] * proj[1] + modl[9] * proj[5] + modl[10] * proj[9] + modl[11] * proj[13]
        clip[10] = modl[8] * proj[2] + modl[9] * proj[6] + modl[10] * proj[10] + modl[11] * proj[14]
        clip[11] = modl[8] * proj[3] + modl[9] * proj[7] + modl[10] * proj[11] + modl[11] * proj[15]

        clip[12] = modl[12] * proj[0] + modl[13] * proj[4] + modl[14] * proj[8] + modl[15] * proj[12]
        clip[13] = modl[12] * proj[1] + modl[13] * proj[5] + modl[14] * proj[9] + modl[15] * proj[13]
        clip[14] = modl[12] * proj[2] + modl[13] * proj[6] + modl[14] * proj[10] + modl[15] * proj[14]
        clip[15] = modl[12] * proj[3] + modl[13] * proj[7] + modl[14] * proj[11] + modl[15] * proj[15]

        # Right plane
        frustum[0] = clip[3] - clip[0]
        frustum[1] = clip[7] - clip[4]
        frustum[2] = clip[11] - clip[8]
        frustum[3] = clip[15] - clip[12]

        # Left plane
        frustum[4] = clip[3] + clip[0]
        frustum[5] = clip[7] + clip[4]
        frustum[6] = clip[11] + clip[8]
        frustum[7] = clip[15] + clip[12]

        # Bottom plane
        frustum[8] = clip[3] + clip[1]
        frustum[9] = clip[7] + clip[5]
        frustum[10] = clip[11] + clip[9]
        frustum[11] = clip[15] + clip[13]

        # Top plane
        frustum[12] = clip[3] - clip[1]
        frustum[13] = clip[7] - clip[5]
        frustum[14] = clip[11] - clip[9]
        frustum[15] = clip[15] - clip[13]

        # Far plane
        frustum[16] = clip[3] - clip[2]
        frustum[17] = clip[7] - clip[6]
        frustum[18] = clip[11] - clip[10]
        frustum[19] = clip[15] - clip[14]
        # Custom far plane
        # frustum[16] = clip[2] * (-far_plane) + clip[3]
        # frustum[17] = clip[6] * (-far_plane) + clip[7]
        # frustum[18] = clip[10] * (-far_plane) + clip[11]
        # frustum[19] = clip[14] * (-far_plane) + clip[15]
        # Custom far plane
        # frustum[16] = clip[2] * far_plane + clip[3]
        # frustum[17] = clip[6] * far_plane + clip[7]
        # frustum[18] = clip[10] * far_plane + clip[11]
        # frustum[19] = clip[14] * far_plane + clip[15]


        # Custom near plane
        frustum[20] = clip[2] * near_plane + clip[3]
        frustum[21] = clip[6] * near_plane + clip[7]
        frustum[22] = clip[10] * near_plane + clip[11]
        frustum[23] = clip[14] * near_plane + clip[15]
        # Near plane
        # frustum[20] = clip[3] + clip[2]
        # frustum[21] = clip[7] + clip[6]
        # frustum[22] = clip[11] + clip[10]
        # frustum[23] = clip[15] + clip[14]
        # Custom near plane
        # frustum[20] = clip[2] * near_plane + clip[3]
        # frustum[21] = clip[6] * near_plane + clip[7]
        # frustum[22] = clip[10] * near_plane + clip[11]
        # frustum[23] = clip[14] * near_plane + clip[15]

        return frustum

    def cube_in_frustum(self, x, y, z, size, frustum):
        for p in range(0, 24, 4):
            if frustum[p] * (x - size) + frustum[p + 1] * (y - size) + frustum[p + 2] * (z - size) + frustum[p + 3] > 0:
                continue
            if frustum[p] * (x + size) + frustum[p + 1] * (y - size) + frustum[p + 2] * (z - size) + frustum[p + 3] > 0:
                continue
            if frustum[p] * (x - size) + frustum[p + 1] * (y + size) + frustum[p + 2] * (z - size) + frustum[p + 3] > 0:
                continue
            if frustum[p] * (x + size) + frustum[p + 1] * (y + size) + frustum[p + 2] * (z - size) + frustum[p + 3] > 0:
                continue
            if frustum[p] * (x - size) + frustum[p + 1] * (y - size) + frustum[p + 2] * (z + size) + frustum[p + 3] > 0:
                continue
            if frustum[p] * (x + size) + frustum[p + 1] * (y - size) + frustum[p + 2] * (z + size) + frustum[p + 3] > 0:
                continue
            if frustum[p] * (x - size) + frustum[p + 1] * (y + size) + frustum[p + 2] * (z + size) + frustum[p + 3] > 0:
                continue
            if frustum[p] * (x + size) + frustum[p + 1] * (y + size) + frustum[p + 2] * (z + size) + frustum[p + 3] > 0:
                continue
            return False
        return True