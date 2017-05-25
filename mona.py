#!/usr/bin/env python
import pygame
from PIL import Image

import copy
from itertools import izip
from os import path
import random
import sys

import lib.ptvLIB as ptv # for drawing transparent polygons in Pygame


class Polygon(object):
    def __init__(self, alpha):
        self.points = []
        self.color = [0,0,0]
        self.alpha = alpha


class Control(object):
    """This is a general controller object/interface for the program."""

    def __init__(self, filepath):
        pygame.init()
        self.clock = pygame.time.Clock()

        # maybe try/exc here?
        # split the arg by slashes to enable dirs
        self.seed = pygame.image.load(path.join(filepath))
        self.canvas = self.seed.copy() # copy and ...
        self.canvas.fill((0,0,0))      # ... clear it so it matchs the bit-depth of seed
        self.canvas_rect = self.canvas.get_rect()
        self.seed_rect = self.seed.get_rect(left=self.seed.get_width())

        self.SCREEN_W = self.seed.get_width() * 2
        self.SCREEN_H = self.seed.get_height()
        self.dna = self.generate_dna()

        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H))
        pygame.display.set_caption("Image evolver")

        self.SCREEN.blit(self.seed, self.seed_rect)

        # color constants
        self.WHITE = pygame.Color(255, 255, 255)


    def generate_dna(self, polygons=100, vertices=6, alpha=50):
        dna = []
        for i in range(polygons):
            poly = Polygon(alpha)
            for j in range(vertices):
                poly.points.append([
                    random.randint(0, self.SCREEN_W/2),
                    random.randint(0, self.SCREEN_H)
                ])
            dna.append(poly)
        return dna

    def draw_polygons(self):
        for polygon in self.dna:
            ptv.draw_alpha_polygon(self.canvas, polygon.color, (0,0), polygon.points, polygon.alpha)


    def mutate(self):
        """Make a random mutation to a randomly-chosen attribute of a
        randomly-chosen polygon"""
        polygon = random.choice(self.dna)
        # a dice roll is decidedly random
        diceroll = random.randint(0,1)
        if diceroll == 0:
            polygon.points[random.randint(0, len(polygon.points)-1)] = [random.randint(0, self.SCREEN_W/2), random.randint(0, self.SCREEN_H)]
        if diceroll == 1:
            polygon.color[random.randint(0, 2)] = random.randint(0, 255)
        # if diceroll == 2:
        #     polygon.alpha = random.randint(0,100)


    def compare_surfaces(self, pg_canvas, pg_seed):
        """Returns a percentage. 0% means there is no difference between the
        two images, 100% means the images are opposites"""

        canvas_str = pygame.image.tostring(pg_canvas, "RGBA")
        seed_str = pygame.image.tostring(pg_seed, "RGBA")

        i_canvas = Image.fromstring("RGBA", pg_canvas.get_size(), canvas_str)
        i_seed = Image.fromstring("RGBA", pg_seed.get_size(), seed_str)

        pairs = izip(i_canvas.getdata(), i_seed.getdata())

        if len(i_canvas.getbands()) == 1:
            # grayscale
            dif = sum(abs(p1-p2) for p1,p2 in pairs)
        else:
            # color
            dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

        ncomponents = i_canvas.size[0] * i_canvas.size[1] * 3
        return (dif / 255.0 * 100) / ncomponents

    def loop(self):
        """This is the infinite loop of the program"""
        while True:

            # store 'mother' values in case she is more fit than 'daughter'
            previous_surface = self.canvas.copy()
            previous_dna = copy.deepcopy(self.dna)

            self.canvas.fill(self.WHITE)
            self.mutate() # this should alter self.dna
            self.draw_polygons() # this should alter self.canvas

            self.SCREEN.blit(self.canvas, self.canvas_rect) # draw it for visual response--better or worse

            # differences between surfaces and self.seed
            previous_difference = self.compare_surfaces(previous_surface, self.seed)
            current_difference = self.compare_surfaces(self.canvas, self.seed)

            # keep whichever DNA is more fit
            if previous_difference < current_difference:
                self.dna = copy.deepcopy(previous_dna)

            current_fitness = self.compare_surfaces(self.canvas, self.seed)
            print "Current fitness: {}%".format(100-current_difference)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(120)
