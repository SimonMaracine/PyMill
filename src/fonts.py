"""Module that stores all declared fonts. Should imported where font objects are needed."""

import pygame

pygame.font.init()

board_font = pygame.font.SysFont("", 30, True)
fps_font = pygame.font.SysFont("", 18, True)
connstatus_font = pygame.font.SysFont("", 30, True)
text_entry_font = pygame.font.SysFont("", 32, True)
button_font = pygame.font.SysFont("", 50, True)
small_button_font = pygame.font.SysFont("", 36, True)
title_font = pygame.font.SysFont("", 70, True)
small_title_font = pygame.font.SysFont("", 62, True)
