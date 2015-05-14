#!/usr/bin/env python
import pygame
import Image

from itertools import izip
from os import path
import sys

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



if __name__ == '__main__':
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

    SCREENW = seed.get_width() * 2
    SCREENH = seed.get_height()
    SCREEN = pygame.display.set_mode((SCREENW, SCREENH))
    pygame.display.set_caption('Image evolver')

    SCREEN.blit(seed, seed_rect)

    # color constants
    WHITE = pygame.Color(255, 255, 255)

while True:
    canvas.fill(WHITE) # actually only fill the surface we are working on

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
