
# utils/asset_loader.py
import pygame
import os

def load_image(filename):
    return pygame.image.load(os.path.join('assets', 'images', filename))

def load_sound(filename):
    return os.path.join('assets', 'sounds', filename)