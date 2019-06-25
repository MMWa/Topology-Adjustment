from typing import Tuple

import pygame
from pygame import gfxdraw
from pygame import *

from simulation.node.Node import NodeType


class WindowManager:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    size = [1200, 800]

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.surface_background = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
        self.surface_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
        self.surface_nodes = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        pygame.display.set_caption("Proof of Concept Demo")

        self.done = False

        self.greedy_relays = []
        self.pursue_relays = []
        self.nodes = []

        self.selection = 0

        self.window_offset = 200

    def catch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.KEYDOWN:
                return event.key

    def tick(self, algorithm_delta=None):
        if not self.done:
            # draw to buffer
            self.__draw(algorithm_delta)

            # flip buffer to screen
            pygame.display.flip()
            self.greedy_relays = []
            self.pursue_relays = []
            self.nodes = []

    def __draw(self, algorithm_delta):
        # Clear the screen and set the screen background
        self.surface_background.fill(self.WHITE)
        self.surface_overlay.fill((0, 0, 0, 0))
        self.surface_nodes.fill((255, 255, 255, 0))

        point_radius = 8
        point_height = point_radius * 2

        # for x in self.greedy_relays:
        #     pygame.draw.circle(self.surface_overlay, (0, 0, 0, 20), self.to_pygame(x, 20), 40, 1)

        for x in self.pursue_relays:
            pygame.draw.circle(self.surface_nodes, self.GREEN, self.to_pygame(x, point_height), point_radius)

        for x in self.greedy_relays:
            pygame.draw.circle(self.surface_nodes, self.BLUE, self.to_pygame(x, point_height), point_radius)

        for x in self.nodes:
            if x == self.selection:
                pygame.draw.circle(self.surface_nodes, self.BLACK, self.to_pygame(x, point_height), point_radius)
            else:
                pygame.draw.circle(self.surface_nodes, self.RED, self.to_pygame(x, point_height), point_radius)

        textsurface1 = self.myfont.render("relay count: " + str(len(self.greedy_relays)), False, (0, 0, 0))
        textsurface2 = self.myfont.render("relay count: " + str(len(self.pursue_relays)), False, (0, 0, 0))
        textsurfaceT = self.myfont.render("execution time:" + str(algorithm_delta) + "s", False, (0, 0, 0))

        self.screen.blit(self.surface_background, (0, 0))
        self.screen.blit(self.surface_overlay, (0, 0))
        self.screen.blit(self.surface_nodes, (0, 0))
        self.screen.blit(textsurface1, (0, 0))
        self.screen.blit(textsurface2, (0, 30))

        self.screen.blit(textsurfaceT, (0, 60))

    def to_pygame(self, coords, obj_height):
        """Convert an object's coords into pygame coordinates (lower-left of object => top left in pygame coords)."""
        return coords[0] + self.window_offset, (self.size[1] - self.window_offset) - coords[1] - obj_height

    def quit(self):
        pygame.quit()


class WindowManagerTypeTwo:
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    RED: Tuple[int, int, int] = (255, 0, 0)
    PALE_BLUE: Tuple[int, int, int] = (0, 204, 204)

    GREEDY_RELAY_COLOR = GREEN
    NODE_COLOR = RED
    ALGO_RELAY_COLOR = BLUE

    SElECTED_NODE = BLACK
    BACKGROUND = WHITE
    LINK = PALE_BLUE

    # BLACK = (0, 0, 0)
    # WHITE = (255, 255, 255)
    # BLUE = pygame.Color("#5a05d4")
    # GREEDY_RELAY_COLOR = (149, 152, 159)
    # NODE_COLOR = (149, 152, 159)
    # RED = (255, 0, 0)
    # PALE_BLUE = (0, 204, 204)

    size = [1200, 800]

    def __init__(self):
        self.caller_toggle = True
        self.follower_toggle = True
        self.environment_toggle = True
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.surface_background = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
        self.surface_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
        self.surface_nodes = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        pygame.display.set_caption("Proof of Concept Demo")

        self.done = False

        self.greedy_relays = []
        self.pursue_relays = []
        self.nodes = []

        self.selection = 0

        self.window_offset = 200

    def event_pump(self):
        key_seq = []
        done = False
        while not done:

            pygame.event.pump()
            keys = pygame.key.get_pressed()
            print(keys)
            if keys[K_RETURN]:
                done = True
                return

    def catch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.KEYDOWN:
                return event.key

    def tick(self, algorithm_delta=None):
        if not self.done:
            # draw to buffer
            self.__draw(algorithm_delta)

            # flip buffer to screen
            pygame.display.flip()
            self.greedy_relays = []
            self.pursue_relays = []
            self.nodes = []

    def __draw(self, algorithm_delta):
        # Clear the screen and set the screen background
        self.surface_background.fill(self.BACKGROUND)
        self.surface_overlay.fill((0, 0, 0, 0))
        self.surface_nodes.fill((255, 255, 255, 0))

        point_radius = 8
        point_height = point_radius * 2

        # pursue_relays and greedy_relays should be switched everything will make sense then.
        for x in self.pursue_relays:
            pygame.draw.circle(self.surface_nodes, self.GREEDY_RELAY_COLOR, self.to_pygame(x, point_height),
                               int(point_radius / 2))

        for y in self.greedy_relays:
            x = y.position.as_int_array
            # z = y.follower.position.as_int_array
            # w = y.last_caller.position.as_int_array
            env_list = y.children

            if self.environment_toggle:
                for ii_e in env_list:
                    pygame.draw.line(self.surface_overlay, self.LINK, self.to_pygame(x, point_height),
                                     self.to_pygame(ii_e.position.as_int_array, point_height), 2)

            pygame.draw.circle(self.surface_nodes, self.ALGO_RELAY_COLOR, self.to_pygame(x, point_height), point_radius)
            pygame.draw.circle(self.surface_overlay, (0, 0, 0, 20), self.to_pygame(x, 20), 40, 1)
            #
            # if self.follower_toggle or self.caller_toggle:
            #     pygame.draw.circle(self.surface_nodes, self.PALE_BLUE, self.to_pygame([x[0],x[1]+24], 0), 2)

            # if self.follower_toggle:
            #     pygame.draw.line(self.surface_nodes,self.PALE_BLUE, self.to_pygame([x[0],x[1]+24], 2), self.to_pygame(z, point_height))
            # if self.caller_toggle:
            #     pygame.draw.line(self.surface_nodes,self.RED, self.to_pygame([x[0],x[1]+24], 2), self.to_pygame(w, point_height))

        for y in self.nodes:

            x = y.position.as_int_array

            if x == self.selection:
                pygame.draw.circle(self.surface_nodes, self.SElECTED_NODE, self.to_pygame(x, point_height),
                                   point_radius)
            else:
                pygame.draw.circle(self.surface_nodes, self.NODE_COLOR, self.to_pygame(x, point_height), point_radius)
            if y.type == NodeType.End:

                z = y.parent.position.as_int_array
                env_list = y.children

                pygame.draw.circle(self.surface_nodes, self.PALE_BLUE, self.to_pygame([x[0], x[1] + 24], 0), 2)
                pygame.draw.line(self.surface_overlay, self.PALE_BLUE, self.to_pygame([x[0], x[1] + 24], 2),
                                 self.to_pygame(z, point_height))
                for ii_e in env_list:
                    pygame.draw.line(self.surface_nodes, (255, 153, 51), self.to_pygame(x, point_height),
                                     self.to_pygame(ii_e.position.as_int_array, point_height))

        textsurface1 = self.myfont.render("relay count: " + str(len(self.greedy_relays)), False, (0, 0, 0))
        textsurface2 = self.myfont.render("relay count: " + str(len(self.pursue_relays)), False, (0, 0, 0))
        textsurfaceT = self.myfont.render("execution time:" + str(algorithm_delta) + "s", False, (0, 0, 0))

        self.screen.blit(self.surface_background, (0, 0))
        self.screen.blit(self.surface_overlay, (0, 0))
        self.screen.blit(self.surface_nodes, (0, 0))
        self.screen.blit(textsurface1, (0, 0))
        self.screen.blit(textsurface2, (0, 30))

        self.screen.blit(textsurfaceT, (0, 60))

    def to_pygame(self, coords, obj_height):
        """Convert an object's coords into pygame coordinates (lower-left of object => top left in pygame coords)."""
        return coords[0] + self.window_offset, (self.size[1] - self.window_offset) - coords[1] - obj_height

    def quit(self):
        pygame.quit()


class WindowManagerTypeThree:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    PALE_BLUE = (0, 204, 204)

    size = [1200, 800]

    def __init__(self):
        self.caller_toggle = True
        self.follower_toggle = True
        self.environment_toggle = True
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.surface_background = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
        self.surface_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)
        self.surface_nodes = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA, 32)

        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)

        pygame.display.set_caption("Proof of Concept Demo")

        self.done = False

        self.greedy_relays = []
        self.pursue_relays = []
        self.nodes = []

        self.selection = 0

        self.window_offset = 200

    def catch_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.KEYDOWN:
                return event.key

    def tick(self, algorithm_delta=None):
        if not self.done:
            # draw to buffer
            self.__draw(algorithm_delta)

            # flip buffer to screen
            pygame.display.flip()
            self.greedy_relays = []
            self.pursue_relays = []
            self.nodes = []

    def __draw(self, algorithm_delta):
        # Clear the screen and set the screen background
        self.surface_background.fill(self.WHITE)
        self.surface_overlay.fill((0, 0, 0, 0))
        self.surface_nodes.fill((255, 255, 255, 0))

        point_radius = 8
        point_height = point_radius * 2

        for x in self.pursue_relays:
            pygame.draw.circle(self.surface_nodes, self.GREEN, self.to_pygame(x, point_height), point_radius)

        for y in self.greedy_relays:
            x = y.position.as_int_array
            # z = y.follower.position.as_int_array
            # w = y.last_caller.position.as_int_array
            env_list = y.children

            if self.environment_toggle:
                for ii_e in env_list:
                    pygame.draw.line(self.surface_nodes, (255, 153, 51), self.to_pygame(x, point_height),
                                     self.to_pygame(ii_e.position.as_int_array, point_height), 5)

            pygame.draw.circle(self.surface_nodes, self.BLUE, self.to_pygame(x, point_height), point_radius)
            pygame.draw.circle(self.surface_overlay, (0, 0, 0, 20), self.to_pygame(x, 20), 40, 1)

            if self.follower_toggle or self.caller_toggle:
                pygame.draw.circle(self.surface_nodes, self.PALE_BLUE, self.to_pygame([x[0], x[1] + 24], 0), 2)

            # if self.follower_toggle:
            #     pygame.draw.line(self.surface_nodes,self.PALE_BLUE, self.to_pygame([x[0],x[1]+24], 2), self.to_pygame(z, point_height))
            # if self.caller_toggle:
            #     pygame.draw.line(self.surface_nodes,self.RED, self.to_pygame([x[0],x[1]+24], 2), self.to_pygame(w, point_height))

        for y in self.nodes:

            x = y.position.as_int_array

            if x == self.selection:
                pygame.draw.circle(self.surface_nodes, self.BLACK, self.to_pygame(x, point_height), point_radius)
            else:
                pygame.draw.circle(self.surface_nodes, self.RED, self.to_pygame(x, point_height), point_radius)
            if y.type == NodeType.End:

                z = y.follower.position.as_int_array
                env_list = y.children

                pygame.draw.circle(self.surface_nodes, self.PALE_BLUE, self.to_pygame([x[0], x[1] + 24], 0), 2)
                pygame.draw.line(self.surface_nodes, self.PALE_BLUE, self.to_pygame([x[0], x[1] + 24], 2),
                                 self.to_pygame(z, point_height))
                for ii_e in env_list:
                    pygame.draw.line(self.surface_nodes, (255, 153, 51), self.to_pygame(x, point_height),
                                     self.to_pygame(ii_e.position.as_int_array, point_height))

        textsurface1 = self.myfont.render("relay count: " + str(len(self.greedy_relays)), False, (0, 0, 0))
        textsurface2 = self.myfont.render("relay count: " + str(len(self.pursue_relays)), False, (0, 0, 0))
        textsurfaceT = self.myfont.render("execution time:" + str(algorithm_delta) + "s", False, (0, 0, 0))

        self.screen.blit(self.surface_background, (0, 0))
        self.screen.blit(self.surface_overlay, (0, 0))
        self.screen.blit(self.surface_nodes, (0, 0))
        self.screen.blit(textsurface1, (0, 0))
        self.screen.blit(textsurface2, (0, 30))

        self.screen.blit(textsurfaceT, (0, 60))

    def to_pygame(self, coords, obj_height):
        """Convert an object's coords into pygame coordinates (lower-left of object => top left in pygame coords)."""
        return coords[0] + self.window_offset, (self.size[1] - self.window_offset) - coords[1] - obj_height

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    game_window = WindowManager()
    game_window.tick()
    game_window.tick()
    game_window.quit()
