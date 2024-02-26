import pygame
import random

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Set display dimensions
dis_width = 800
dis_height = 600

# Initialize pygame
pygame.init()

# Create display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def gameLoop():
    game_over = False
    game_close = False

    # Initialize snake position
    snake_pos = [[100, 50], [90, 50], [80, 50], [70, 50]]
    snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
    food_pos = [random.randrange(1, (dis_width - snake_block) // 10) * 10,
                 random.randrange(1, (dis_height - snake_block) // 10) * 10]
    food_spawn = True

    while not game_over:
        while game_close:
            dis.fill(black)
            message("You Lost! Press Q to quit or C to play again.", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake_pos[0][0] -= snake_block
                elif event.key == pygame.K_RIGHT:
                    snake_pos[0][0] += snake_block
                elif event.key == pygame.K_UP:
                    snake_pos[0][1] -= snake_block
                elif event.key == pygame.K_DOWN:
                    snake_pos[0][1] += snake_block

                new_pos = snake_pos[0].copy()
                snake_pos.insert(0, new_pos)

                if snake_pos[0][0] == food_pos[0] and snake_pos[0][1] == food_pos[1]:
                    food_spawn = False
                else:
                    snake_pos.pop()

                if snake_pos[0][0] < 0 or snake_pos[0][0] >= dis_width or snake_pos[0][1] < 0 or snake_pos[0][1] >= dis_height:
                    game_close = True

                for block in snake_pos[1:]:
                    if snake_pos[0] == block:
                        game_close = True

                if food_spawn == False:
                    food_pos = [random.randrange(1, (dis_width - snake_block) // 10) * 10,
                                 random.randrange(1, (dis_height - snake_block) // 10) * 10]

        dis.fill(black)
        for pos in