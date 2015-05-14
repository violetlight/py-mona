#!/usr/bin/env python
import pygame
import Image

from itertools import izip
from os import path
import random
import sys

import lib.ptvLIB as ptv # for transparent polygons


class Polygon(object):
    def __init__(self, alpha):
        self.points = []
        self.color = [0,0,0]
        self.alpha = alpha



def mutate(dna):
    polygon = random.choice(dna)

    # a dice roll is decidedly random
    diceroll = random.randint(0,2)
    if diceroll == 0:
        polygon.points[random.randint(0, len(polygon.points)-1)] = [random.randint(0, SCREEN_W/2), random.randint(0, SCREEN_H)]
    if diceroll == 1:
        polygon.color[random.randint(0, 2)] = random.randint(0, 255)
    if diceroll == 2:
        polygon.alpha = random.randint(0,100)


def compare_surfaces(pg_canvas, pg_seed):
    canvas_str = pygame.image.tostring(pg_canvas, "RGBA")
    seed_str = pygame.image.tostring(pg_seed, "RGBA")

    i_canvas = Image.fromstring("RGBA", pg_canvas.get_size(), canvas_str)
    i_seed = Image.fromstring("RGBA", pg_seed.get_size(), seed_str)

    pairs = izip(i_canvas.getdata(), i_seed.getdata())

    if len(i_canvas.getbands()) == 1:
        # grayscale
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        #color
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))

    ncomponents = i_canvas.size[0] * i_canvas.size[1] * 3
    print "Difference (percentage):", (dif / 255.0 * 100) / ncomponents



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "ERROR: Provide a path to an image as the only argument."
        sys.exit()

    pygame.init()
    clock = pygame.time.Clock()

    # maybe try/exc here?
    # split the arg by slashes to enable dirs
    seed = pygame.image.load(path.join(sys.argv[1]))
    canvas = seed.copy() # copy and clear so it matches bit depth of seed
    canvas_rect = canvas.get_rect()
    canvas.fill((0,0,0))
    seed_rect = seed.get_rect(left=seed.get_width())

    # need to use pygame surfarrays

    SCREEN_W = seed.get_width() * 2
    SCREEN_H = seed.get_height()
    SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Image evolver")

    SCREEN.blit(seed, seed_rect)

    # color constants
    WHITE = pygame.Color(255, 255, 255)


def generate_dna(polygons=50, vertices=4, alpha=50):
    dna = []
    for i in range(polygons):
        poly = Polygon(alpha)
        for j in range(vertices):
            poly.points.append([
                random.randint(0, SCREEN_W/2),
                random.randint(0, SCREEN_H)
            ])
        dna.append(poly)
    return dna

def draw_polygons(dna):
    for polygon in dna:
        ptv.draw_alpha_polygon(canvas, polygon.color, (0,0), polygon.points, polygon.alpha)

dna = generate_dna()
while True:
    canvas.fill(WHITE) # actually only fill the surface we are working on
    mutate(dna)
    draw_polygons(dna)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                compare_surfaces(canvas, seed)

    SCREEN.blit(canvas, canvas_rect)

    pygame.display.update()
    clock.tick(30)
