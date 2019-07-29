"""Module that stores all declared fonts. Should imported where font objects are needed."""

import pygame

pygame.font.init()

board_font = pygame.font.SysFont("calibri", 30, True)
fps_font = pygame.font.SysFont("calibri", 18, True)
connstatus_font = pygame.font.SysFont("calibri", 30, True)
text_entry_font = pygame.font.SysFont("calibri", 32, True)
