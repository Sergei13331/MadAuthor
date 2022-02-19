import pygame
from pygame import gfxdraw
import numpy as np
import glm

import threading
from time import sleep
import time
import random

import verticles


objects = []
text = []


class GameObject:
    def __init__(self, position=verticles.cube):
        self.position = position
        self.transform = glm.mat4()

        self.color = [0, 150, 90]

    def fixed_update(self):
        pass
        # angle = 4 * time.time_ns() / 10 ** 10 % (np.pi * 2)
        # self.transform = glm.rotate(angle, glm.vec3(0, 1, 0)) * glm.rotate(glm.radians(45), glm.vec3(1, 0, 1))


class FigureObject(GameObject):
    def __init__(self, position=verticles.cube, coords=(0, 0, 0)):
        super(FigureObject, self).__init__(position)
        self.transform = glm.scale(glm.vec3(0.3)) * glm.rotate(random.random() * 360, glm.vec3(random.random(), random.random(), random.random())) * glm.translate(glm.vec3(coords))
    
    def fixed_update(self):
        pass


class Camera:
    def __init__(self, fov=90., near_plane=0.1, far_plane=100., aspect_ratio=16/9):
        self.fov = glm.radians(fov)
        self.near_plane = near_plane
        self.far_plane = far_plane
        self.aspect_ratio = aspect_ratio

        self.view = glm.translate(glm.vec3(0, 0, -3)) * glm.scale(glm.vec3(0.3))
        self.projection = glm.perspective(self.fov, self.aspect_ratio, near_plane, far_plane)

    def fixed_update(self):
        self.projection = glm.perspective(self.fov, self.aspect_ratio, self.near_plane, self.far_plane)


class Engine:
    def __init__(self, width=800, height=600):
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont('Times New Roman', 30)
        self.screen_size = width, height
        self.surface = pygame.display.set_mode(self.screen_size)
        self.background = (30, 100, 140)

        self.main_camera = Camera(aspect_ratio=width/height)

    def draw_polygon(self, color, tri):
        tri = tuple((round(a[0] * self.screen_size[0] / 2 + self.screen_size[0] / 2),
                     round(a[1] * self.screen_size[1] / 2 + self.screen_size[1] / 2)) for a in tri)

        for i in range(0, len(tri), 3):
            # gfxdraw.aapolygon(self.surface, (*tri[i][:2], *tri[i + 1][:2], *tri[i + 2][:2]), color)
            gfxdraw.filled_trigon(self.surface, *tri[i][:2], *tri[i + 1][:2], *tri[i + 2][:2], color)
            # gfxdraw.aatrigon(self.surface, *tri[i][:2], *tri[i + 1][:2], *tri[i + 2][:2], pygame.Color(150, 50, 50))

    def run(self):
        score = 0
        flag_fifth = False
        color = 0

        flag_fifth_time = 0

        running = True
        start_flag = False
        last_frame = 0

        camera_rotation_deg = random.random() / 2 + 1
        camera_rotation_axe_x = (random.random() - 0.5) * 2
        camera_rotation_axe_y = (random.random() - 0.5) * 2
        camera_rotation_axe_z = (random.random() - 0.5) * 2

        while running:

            t = pygame.time.get_ticks()
            delta_time = (t - last_frame) / 1000.0
            last_frame = t

            self.surface.fill(self.background)

            if flag_fifth:
                color += flag_fifth_time
                objects[-1].color[0] = color

                if objects[-1].color[0] >= 250:
                    flag_fifth = False
                    color = 0
                    flag_fifth_time = 0

                    running = True
                    start_flag = False
                    last_frame = 0

                    text[0] = ('You loose', text[0][1])
                    text[1] = ('Your score: ' + str(score - 100), text[1][1])
                    text[2] = ('', text[2][1])


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if len(objects) >= 1 and not start_flag:
                            objects.clear()
                            objects.append(FigureObject(position=make_rect(-1, -1, 0, 1, -1, 0, -1, 1, 0, 1, 1, 0)))
                            score = 0

                        if start_flag:
                            pass

                        text[0] = ('', text[0][1])
                        text[1] = ('', text[1][1])
                        text[2] = (str(score), text[2][1])
                        start_flag = True

                        if 10 < objects[-1].color[0] < 150:
                            flag_fifth = False
                            color = 0
                            flag_fifth_time = 0

                            running = True
                            start_flag = False
                            last_frame = 0

                            text[0] = ('You loose', text[0][1])
                            text[1] = ('Your score: ' + str(score - 100), text[1][1])
                            text[2] = ('', text[2][1])

                        else:
                            color = 0

                            score += 100

                            obj = objects[-1]

                            rx, ry, rz = ((random.random() - 0.5) * 2, (random.random() - 0.5) * 2, (random.random() - 0.5) * 6)

                            x1, y1, z1, x2, y2, z2 = (obj.position[-3], obj.position[-2], obj.position[-1],
                                                      obj.position[-6], obj.position[-5], obj.position[-4])
                            obj.position.append(x1)
                            obj.position.append(y1)
                            obj.position.append(z1)
                            obj.position.append(x2)
                            obj.position.append(y2)
                            obj.position.append(z2)
                            obj.position.append(rx)
                            obj.position.append(ry)
                            obj.position.append(rz)

                            flag_fifth = False

                            flag_fifth_time = random.random() / 3 + 0.3

                        if not flag_fifth:

                            FIELD_SIZE = 5

                            rand_x = random.randint(-FIELD_SIZE // 2, FIELD_SIZE // 2) * 2
                            rand_y = random.randint(-FIELD_SIZE // 2, FIELD_SIZE // 2) * 2
                            rand_z = random.randint(-FIELD_SIZE // 2, FIELD_SIZE // 2) * 2

                            rect = make_rect(-1, -1, 0, 1, -1, 0, -1, 1, 0, 1, 1, 0)

                            obj = FigureObject(position=rect, coords=(rand_x, rand_y, rand_z))
                            objects.append(obj)

                            # self.main_camera.view = obj.transform

                            flag_fifth = True


            if start_flag:
                self.main_camera.view = self.main_camera.view * glm.rotate(delta_time * camera_rotation_deg,
                                                                           glm.vec3(camera_rotation_axe_x, camera_rotation_axe_y, camera_rotation_axe_z))

            self.main_camera.fixed_update()

            for obj in objects:
                obj.fixed_update()
                screenspace_model_matrix = self.main_camera.projection * self.main_camera.view * obj.transform
                poly = []
                for i in range(0, len(obj.position), 3):
                    pos_vec4 = screenspace_model_matrix * glm.vec4(*obj.position[i:i + 3], 1.)
                    poly.append(pos_vec4)
                self.draw_polygon(obj.color, poly)

            for string in text:
                text_surface = self.font.render(string[0], False, (230, 230, 230))
                self.surface.blit(text_surface, string[1])

            pygame.display.flip()

    def __del__(self):
        pygame.quit()


def make_rect(*pos):
    return [*pos[:3], *pos[3:6], *pos[6:9], *pos[9:], *pos[3:6], *pos[6:9]]


if __name__ == '__main__':

    ### ###
    ### SETTINGS
    ### ###

    SCREEN_RESOLUTION = 1280, 720

    ### ###
    ### ###
    ### ###

    engine = Engine(width=SCREEN_RESOLUTION[0], height=SCREEN_RESOLUTION[1])

    aspect_ratio = SCREEN_RESOLUTION[0] / SCREEN_RESOLUTION[1]

    rect = make_rect(-1, -1, 0, 1, -1, 0, -1, 1, 0, 1, 1, 0)

    obj1 = FigureObject(position=rect)
    objects.append(obj1)
    text.append(('PRESS SPACE TO START', (SCREEN_RESOLUTION[0] // 2 - 120 * aspect_ratio, SCREEN_RESOLUTION[1] // 2)))
    text.append(('', (SCREEN_RESOLUTION[0] // 2 - 120 * aspect_ratio, SCREEN_RESOLUTION[1] // 1.5)))
    text.append(('', (0, 0)))

    # thr_render1 = threading.Thread(target=engine.run)
    # thr_render1.start()

    engine.run()
