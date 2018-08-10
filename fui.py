import pygame


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

        for x in self.greedy_relays:
            pygame.draw.circle(self.surface_overlay, (0, 0, 0, 20), self.to_pygame(x, 20), 40,1)

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
        return (coords[0] + self.window_offset, (self.size[1] - self.window_offset) - coords[1] - obj_height)

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    game_window = WindowManager()
    game_window.tick()
    game_window.tick()
    game_window.quit()
