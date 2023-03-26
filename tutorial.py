import pygame
from player import Player
from objects import Block, Fire
from helpers import get_background, draw, generate_blocks
from helpers_player import handle_move
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 60

window = pygame.display.set_mode((WIDTH, HEIGHT))

def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background(WIDTH, HEIGHT, "Blue.png")

    block_size = 96

    player = Player(100, 100, 50, 50)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size), fire]
    generate_blocks(objects, 3, block_size, "vertical", height_off=4, blocks_distance=0, HEIGHT=HEIGHT, Block=Block)
    generate_blocks(objects, 4, block_size, "horizontal", height_off=4, blocks_distance=5,  HEIGHT=HEIGHT, Block=Block)
    generate_blocks(objects, 6, block_size, "horizontal", height_off=5, blocks_distance=10,  HEIGHT=HEIGHT, Block=Block)

    offset_x = 0
    scroll_area_width = 200

    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x, HEIGHT)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
