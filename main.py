import pygame
import sys
import noise
import random
import math
from pygame.locals import *

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Infinite Terrain Generation")

USE_SPRITES = False
RENDER_DISTANCE = 32
PLAYER_SPEED = 5

WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (105, 105, 105)


def load_image(path, default_shape, color=None):
    if USE_SPRITES:
        try:
            image = pygame.image.load(path).convert_alpha()
            image = pygame.transform.scale(image, default_shape)
            return image
        except pygame.error:
            print("Error loading image:", path)
    shape = pygame.Surface(default_shape, pygame.SRCALPHA)
    if color:
        shape.fill(color)
    return shape


PLAYER_IMG = load_image('player_sprite.png', (40, 40), (255, 100, 0))
WATER_IMG = load_image('water_sprite.png', (20, 20), BLUE)
GRASS_IMG = load_image('grass_sprite.png', (20, 20), GREEN)
STONE_IMG = load_image('stone_sprite.png', (20, 20), GRAY)
DIRT_IMG = load_image('dirt_sprite.png', (20, 20), BROWN)
SAND_IMG = load_image('sand_sprite.png', (20, 20), (255, 255, 0))
FOREST_IMG = load_image('forest_sprite.png', (20, 20), GREEN)
SNOW_IMG = load_image('snow_sprite.png', (20, 20), WHITE)

HEART_IMG = pygame.Surface((30, 30), pygame.SRCALPHA)
HEART_IMG.fill(RED)

def generate_chunk(player_pos, seed):
    chunk = []
    player_chunk_x, player_chunk_y = player_pos[0] // 16, player_pos[1] // 16

    random.seed(seed)

    for y in range(player_chunk_y - RENDER_DISTANCE // 2, player_chunk_y + RENDER_DISTANCE // 2):
        row = []
        for x in range(player_chunk_x - RENDER_DISTANCE // 2, player_chunk_x + RENDER_DISTANCE // 2):
            chunk_x = x * 16
            chunk_y = y * 16
            distance = math.sqrt(
                (player_pos[0] - chunk_x) ** 2 + (player_pos[1] - chunk_y) ** 2)

            if distance <= RENDER_DISTANCE * 8:
                noise_val = noise.pnoise2(
                    chunk_x / 100.0, chunk_y / 100.0, octaves=6)

                if noise_val < -0.4:
                    tile_image = WATER_IMG  # Deep Ocean
                elif noise_val < -0.3:
                    tile_image = WATER_IMG  # Ocean
                elif noise_val < -0.1:
                    tile_image = WATER_IMG  # Lake
                elif noise_val < 0.05:
                    tile_image = SAND_IMG  # Beach
                elif noise_val < 0.2:
                    tile_image = GRASS_IMG  # Plains
                elif noise_val < 0.5:
                    tile_image = FOREST_IMG  # Forest
                elif noise_val < 0.7:
                    tile_image = STONE_IMG  # Mountains
                else:
                    tile_image = SNOW_IMG  # Snowy Peaks

                row.append(tile_image)
            else:
                row.append(None)
        chunk.append(row)
    return chunk


def draw_world(chunk, player_pos):
    chunk_width = len(chunk[0]) * 20
    chunk_height = len(chunk) * 20

    center_x = (SCREEN_WIDTH - chunk_width) // 2 - (player_pos[0] % 20)
    center_y = (SCREEN_HEIGHT - chunk_height) // 2 - (player_pos[1] % 20)

    for y, row in enumerate(chunk):
        for x, tile_image in enumerate(row):
            if tile_image:
                screen.blit(tile_image, (x * 20 + center_x, y * 20 + center_y))


def draw_hearts(player_health):
    heart_spacing = 40
    for i in range(player_health // 10):
        screen.blit(HEART_IMG, (10 + i * heart_spacing, 10))


# Game setup

# Adjust player image size
PLAYER_SIZE = (20, 20)  # New size of the player image
PLAYER_IMG = pygame.transform.scale(PLAYER_IMG, PLAYER_SIZE)

# Update player rectangle
player_rect = PLAYER_IMG.get_rect(
    center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))


player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
velocity = PLAYER_SPEED
player_health = 100
seed = random.randint(0, 1000)  # Random seed for terrain generation

# Define zoom factor
ZOOM_FACTOR = 2  # You can adjust this value to change the zoom level

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((0, 0, 0))

    # Generate and draw world
    chunk = generate_chunk(player_pos, seed)
    draw_world(chunk, player_pos)

    # Player controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] += velocity
    if keys[pygame.K_RIGHT]:
        player_pos[0] -= velocity
    if keys[pygame.K_UP]:
        player_pos[1] += velocity
    if keys[pygame.K_DOWN]:
        player_pos[1] -= velocity

    # Draw player with zoom
    player_zoomed_size = (
        PLAYER_SIZE[0] * ZOOM_FACTOR, PLAYER_SIZE[1] * ZOOM_FACTOR)
    player_zoomed_img = pygame.transform.scale(PLAYER_IMG, player_zoomed_size)
    player_zoomed_rect = player_zoomed_img.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(player_zoomed_img, player_zoomed_rect)

    # Draw hearts
    draw_hearts(player_health)

    pygame.display.update()
