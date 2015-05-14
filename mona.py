import pygame, sys
from os import path



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
    #create canvas surface

    SCREENW = seed.get_width() * 2
    SCREENH = seed.get_height()
    SCREEN = pygame.display.set_mode((SCREENW, SCREENH))
    pygame.display.set_caption('Image evolver')

    SCREEN.blit(seed, seed_rect)

    # split screen vertically into two surfaces
    # draw it to right surface


    WHITE = pygame.Color(255, 255, 255)

while True:
    canvas.fill(WHITE) # actually only fill the surface we are working on

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    SCREEN.blit(canvas, canvas_rect)

    pygame.display.update()
    clock.tick(30)
