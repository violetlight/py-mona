import pygame, sys

if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    # load sys.argv[1] into image
    seed = pygame.image.load(sys.argv[1])
    SCREENW = seed.get_width() * 2
    SCREENH = seed.get_height()
    # get size of image
    # create screen, set screen dims based on that
    # set caption
    # split screen vertically into two surfaces
    # draw it to right surface
    SCREEN = pygame.display.set_mode((SCREENW, SCREENH))
    pygame.display.set_caption('Image evolver')
    WHITE = pygame.Color(255, 255, 255)

while True:
    SCREEN.fill(WHITE) # actually only fill the surface we are working on

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(30) # pause to run the loop at 30 frames per second
