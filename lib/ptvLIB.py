# ptvLIB copyright (c) 2009 Luke Endres (Fallopiano)
#!/usr/bin/python 
import pygame
from pygame.locals import *
import random
import math
# attempt to import psyco
try: import psyco; psyco.full()
except: pass


# a simple lib to create pygame vectors that have transparency
# enjoy :)

# a simple function to return a surface with alpha properties.
# only made to make code cleaner
def return_surface((width,height),alpha):
     # create our surface
     surface = pygame.Surface((width,height))
     # set all black pixels to transparent
     surface.set_colorkey((0,0,0))
     # apperently adding RLE_ACCEL as a flag to set_alpha
     # greatly increases the speed of per-pixel alpha blitting
     surface.set_alpha(alpha,RLEACCEL)
     return surface

def draw_alpha_rect(screen,color,(x,y),rect,alpha):
     temp_surface = return_surface((rect.width,rect.height),alpha)
     pygame.draw.rect(temp_surface,color,rect)
     screen.blit(temp_surface,(x,y))

     
def draw_alpha_circle(screen,color,(x,y),radius,alpha):
     temp_surface = return_surface((radius*2,radius*2),alpha)
     # draw our circle
     pygame.draw.circle(temp_surface,color,(temp_surface.get_width()/2,temp_surface.get_height()/2),radius)
     screen.blit(temp_surface,(x,y))

def draw_alpha_polygon(screen,color,(x,y),pointlist,alpha):
     # create a surface that you can't see to get polygon rect
     random_surface = return_surface((screen.get_width(),screen.get_height()),0)
     # grab the rect of the polygon.. needs improvment
     rect_of_poly = pygame.draw.polygon(random_surface,(0,0,0),pointlist)
     # create surface
     temp_surface = return_surface((rect_of_poly.width,rect_of_poly.height),alpha)
     # draw polygon
     pygame.draw.polygon(temp_surface,color,pointlist)
     '''temp_surface = return_surface(
          (pygame.draw.polygon(random_surface,color,pointlist).width,
           pygame.draw.polygon(random_surface,color,pointlist).height),
          alpha)'''
     screen.blit(temp_surface,(x,y))
     #print pygame.draw.polygon(screen,(0,0,0),pointlist)
