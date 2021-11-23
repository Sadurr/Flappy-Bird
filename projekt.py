from sense_hat import SenseHat, ACTION_RELEASED
import time
import random
import os


sense = SenseHat()

sense.low_light = True

joystick_up_lock = False

def clamp(x, min_value, max_value):
    return min(max_value, max(x, min_value))

def pushed_up(event):
    global joystick_up_lock
    if event.action != ACTION_RELEASED and joystick_up_lock == False:
        bird.speed -= 2
        joystick_up_lock = True
    if event.action == ACTION_RELEASED:
        joystick_up_lock = False


for i in range(8):
    for j in range(8):
        sense.set_pixel(i, j, 0, 0, 0)

class Bird:
    def __init__(self):
        self.height = 4
        self.speed = 1
        self.x = 2
        self.lives = 3
        self.points = 0


class Obstacle:
    def __init__(self, upper, lower):
        self.upper = upper
        self.lower = lower
        self.x = 7
    
bird = Bird()
sense.stick.direction_up = pushed_up
game_over = False

obstacles = []



while True:
    for i in range(8):
        for j in range(8):
            sense.set_pixel(i, j, 0, 0, 0)
    if bird.height == 7:
        bird.lives -= 1
    bird.height += bird.speed
    bird.height = clamp(bird.height, 0, 7)
    bird.speed = clamp(bird.speed, -1, 1)
    if bird.speed < 1:
        bird.speed += 0.5
    sense.set_pixel(bird.x, int(round(bird.height, 0)), 0, 255, 0)
    for i in obstacles:
        for j in range(i.upper):
            sense.set_pixel(i.x, j, 255, 255, 255)
        for j in range(7, i.lower, -1):
            sense.set_pixel(i.x, j, 255, 255, 255)


        if i.x == bird.x and (bird.height < i.upper or bird.height > i.lower):
            bird.lives -= 1

        if i.x == bird.x and not (bird.height < i.upper or bird.height > i.lower):
            bird.points += 1

        i.x -= 1
        i.x = clamp(i.x, -1, 7)

    for i in obstacles:
        if i.x < 0:
            obstacles.remove(i)
    if not obstacles:
        obstacles.append(Obstacle(random.randint(2, 4), random.randint(5, 7)))
    
    if bird.lives <= 0:
        game_over = True

    if game_over:
        sense.show_message('Game Over', scroll_speed=0.07, text_colour=(255, 0, 0))
        os.system(f'mosquitto_pub -t "Flappy Bird" -m "Ilosc zdobytych punktow: {bird.points}" -h 10.0.50.14')

        obstacles = []
        bird = Bird()
        game_over = False

    time.sleep(0.5)
    print(f"Points: {bird.points} Lives: {bird.lives}")