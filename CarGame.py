import pygame
import os
import sys
import random

os.environ['SDL_VIDEO_CENTERED'] = '0'

pygame.init()

# VARS
WIDTH = 840
HEIGHT = 950
clock = pygame.time.Clock()

x_offset = 0
y_offset = 0

keys = {}
cars_color = []
cars_list = []

game_state = False

score = 0.3
best_score = 0

spawnCarEvt = pygame.USEREVENT

spawnPoint = [182, 306, 430, 558]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CarGame")
pygame.time.set_timer(spawnCarEvt, 500)

# LOAD ASSETS

font = pygame.font.Font('font/Qanelas-Black.ttf', 60)

road_surface = pygame.image.load("assets/road.png")
road_rect = road_surface.get_rect()

start_screen_surface = pygame.transform.scale(pygame.image.load("assets/start.png"), (600, 400))
start_screen_rect = start_screen_surface.get_rect(center= (WIDTH // 2, HEIGHT // 2))

death_screen_surface = pygame.transform.scale(pygame.image.load("assets/death.png"), (600, 400))
death_screen_rect = death_screen_surface.get_rect(center= (WIDTH // 2, HEIGHT // 2))

road_surface = pygame.image.load("assets/road.png")
road_rect = road_surface.get_rect()

yellow_car_surface = pygame.transform.scale(pygame.image.load("assets/yellow.png"), (100, 200))
yellow_car_rect = yellow_car_surface.get_rect(center=(WIDTH // 2, HEIGHT - (HEIGHT // 6)))

green_car_surface = pygame.transform.scale(pygame.image.load("assets/green.png"), (100, 200))
green_car_rect = green_car_surface.get_rect(center=(WIDTH // 2, HEIGHT - (HEIGHT // 6)))

red_car_surface = pygame.transform.scale(pygame.image.load("assets/red.png"), (100, 200))
red_car_rect = red_car_surface.get_rect(center=(WIDTH // 2, HEIGHT - (HEIGHT // 6)))

orange_car_surface = pygame.transform.scale(pygame.image.load("assets/orange.png"), (100, 200))
orange_car_rect = orange_car_surface.get_rect(center=(WIDTH // 2, HEIGHT - (HEIGHT // 6)))


# FUNCTIONS

def display_road():
    screen.blit(road_surface, (0, -road_rect.height + (x_offset % road_rect.height)))
    screen.blit(road_surface, (0, x_offset % road_rect.height))
    screen.blit(road_surface, (0, road_rect.height + (x_offset % road_rect.height)))


def display_car():
    yellow_car_rect.center = (WIDTH // 2 + y_offset, HEIGHT - (HEIGHT // 6))
    screen.blit(yellow_car_surface, yellow_car_rect)


def createCar():
    width = random.choice(spawnPoint)
    return yellow_car_surface.get_rect(x=width, y=-yellow_car_rect.height - random.randint(0, 30))


def display_cars():
    for i, car in enumerate(cars_list):
        if car.width > 400:
            surface = pygame.transform.flip(cars_color[i], False, True)
            screen.blit(surface, car)
        else:
            screen.blit(cars_color[i], car)


def move_cars():
    if len(cars_list) >= 5:
        cars_list.pop(0)
        cars_color.pop(0)
    for i, car in enumerate(cars_list):
        if car.x > 400:
            car.y += 10
        else:
            car.y += 4
    return cars_list, cars_color


def drawText(text):
    if text == "score":
        surface_text = font.render("Score: {}".format(int(score)), True, (255, 255, 255))  # create a fake shadow
        rect_text = surface_text.get_rect(center=(WIDTH // 2, (HEIGHT // 18)))
        screen.blit(surface_text, rect_text)
    if text == "bestscore":
        surface_text = font.render("Meilleur score: {}".format(int(best_score)), True, (255, 255, 255))  # create a fake shadow
        rect_text = surface_text.get_rect(center=(WIDTH // 2, HEIGHT - (HEIGHT // 16)))
        screen.blit(surface_text, rect_text)


def check_collid():
    score_check = score if score > best_score else best_score
    for car in enumerate(cars_list):
        if yellow_car_rect.colliderect(car[1]):
            return False, score_check
    return True, score_check


keys[pygame.K_LEFT] = True
keys[pygame.K_RIGHT] = True

display_road()

while True:

    if game_state:

        game_state, best_score = check_collid()
        if keys.get(pygame.K_LEFT):
            if y_offset < 240:
                y_offset += 4
        if keys.get(pygame.K_RIGHT):
            if y_offset > -240:
                y_offset -= 4

        display_road()
        x_offset += 5

        cars_list, cars_color = move_cars()

        display_cars()
        display_car()

        score += 0.008
        drawText("score")

    if not game_state:

        if best_score > 0:
            drawText("bestscore")
            screen.blit(death_screen_surface, death_screen_rect)
        else:
            screen.blit(start_screen_surface, start_screen_rect)


    for event in pygame.event.get():

        if (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]) or event.type == pygame.KEYDOWN and not game_state:
            game_state = True
            cars_color.clear()
            cars_list.clear()
            pygame.time.set_timer(spawnCarEvt, 500)
            y_offset = 0
            score = 0

        if event.type == spawnCarEvt and game_state:
            color = random.randint(0, 3)
            if color == 0:
                color = yellow_car_surface
            if color == 1:
                color = red_car_surface
            if color == 2:
                color = green_car_surface
            if color == 3:
                color = orange_car_surface

            cars_color.append(color)
            cars_list.append(createCar())
            pygame.time.set_timer(spawnCarEvt, random.randint(800, 1300))

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            keys[event.key] = True

        if event.type == pygame.KEYDOWN:
            keys[event.key] = False

    pygame.display.update()
    clock.tick(80)
