"""This module initializes and stores the important WIDTH, HEIGHT, window and clock variables. Can be import anywhere."""

import pygame

WIDTH = 800
HEIGHT = 600

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simon's Morris")

clock = pygame.time.Clock()
