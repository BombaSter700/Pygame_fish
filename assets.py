import pygame
import os

def load_images(base_path):
    return {
        "restart": pygame.image.load(os.path.join(base_path, "BtnRestart.png")),
        "start": pygame.image.load(os.path.join(base_path, "BtnPlay.png")),
        "count": pygame.image.load(os.path.join(base_path, "FishCounter.png")),
        "enemy": pygame.image.load(os.path.join(base_path, "Fish04_A.png")),
        "enemy_alt": pygame.image.load(os.path.join(base_path, "Fish04_B.png")),
        "player": pygame.image.load(os.path.join(base_path, "Fish01_A.png")),
        "bubble": pygame.image.load(os.path.join(base_path, "Bubble.png")),
        "background": pygame.image.load(os.path.join(base_path, "Scene_A.png")),
        "background_alt": pygame.image.load(os.path.join(base_path, "Scene_B.png")),
    }
