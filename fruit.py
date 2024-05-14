#fungsi menambahkan library yang diperlukan
import pygame
import sys
import os
import time
import random


# Set up game (score, fps game, data buah)
pygame.init()
clock = pygame.time.Clock()
g = 1
nyawa = 3
score = 0
fps = 13
fruits = ['jambu', 'jeruk', 'melon', 'delima', "bomb"]
data = {}

# Set up display (ukuran layar panjang dan lebarnya)
width = 1000
height = 500
white = (255, 255, 255)
black = (0, 0, 0)
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Fruit Ninja")

# fungsi untuk menambahkan bahan bahan game
background_image = pygame.image.load(os.path.join(os.getcwd(),'images/background.jpg'))  # Replace 'background.jpg' with your background image file
background_image = pygame.transform.scale(background_image, (width, height))
sword_cursor = pygame.image.load(os.path.join(os.getcwd(), 'images/sword.png'))  # Replace 'sword_cursor.png' with your sword cursor image file
sword_cursor = pygame.transform.scale(sword_cursor, (50, 50))
font = pygame.font.Font(os.path.join(os.getcwd(), 'images/comic.ttf'), 32)
score_text = font.render(str(score), True, black, white)
lives_icon = pygame.image.load('images/white_lives.png') 
pygame.mixer.music.load(os.path.join(os.getcwd(), 'images/menu.mp3'))


# Fungsi untuk membuat random fruits
def generate_random_fruits(fruit):
    if fruit in "bomb":
        path = os.path.join(os.getcwd(), 'bomb.png')
    else:
        path = os.path.join(os.getcwd(), fruit + '.png')

    data[fruit] = {
        'img': pygame.image.load(path),
        'x': random.randint(100, 500),
        'y': 800,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -60),#control kecepatan throw
        'throw': False,
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False




# Generate initial random fruits
for fruit in fruits:
    generate_random_fruits(fruit)
pygame.mouse.set_visible(False)  # menyembunyikan bentuk cursor defaut
pygame.display.update()



# fungsi menampilkan logo "FRUIT" di menu awal
logo_image = pygame.image.load(os.path.join(os.getcwd(), 'bahan/logo.png'))  # udah 'fruit_ninja_logo.png' sesuai dengan format nama gambar
logo_image = pygame.transform.scale(logo_image, (300, 150))





# Fungsi untuk menghitung jumlah nyawa yang tersisa
def update_nyawa():
    global nyawa
    nyawa -= 1
    if nyawa <= 0:
        game_over()


# Fungsi untuk menampilkan menu Game Over
def game_over():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    start_game() # restart game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit() # keluar dari game

        gameDisplay.blit(background_image, (0, 0))
        game_over_text = font.render("Game Over", True, white)
        gameDisplay.blit(game_over_text, (width // 2 - 150, height // 4))
        menu_text = font.render("Press R to Restart, Q to Quit", True, white)
        gameDisplay.blit(menu_text, (width // 2 - 150, height // 2))
        pygame.display.update()
        clock.tick(15)



# Fungsi untuk display menu awal
def show_menu():
    menu = True

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False

        gameDisplay.blit(background_image, (0, 0))
        gameDisplay.blit(logo_image, (width // 2 - 150, height // 4))  # atur sesuai posisi yang diinginkan
        menu_text = font.render("Press SPACE to Start", True, white)
        gameDisplay.blit(menu_text, (width // 2 - 150, height // 2))
        pygame.display.update()
        clock.tick(15)
pygame.mixer.music.play(-5)





# fungsi utama game 
show_menu()

pygame.mouse.set_visible(False)

while True:
    gameDisplay.blit(background_image, (0, 0))  # fungsi ini mengubah backgroud menjadi background yang kita tambahkan di background_image

    gameDisplay.blit(score_text, (0, 0))

    for key, value in data.items():
        if value['throw']:
            value['x'] = value['x'] + value['speed_x']
            value['y'] = value['y'] + value['speed_y']
            value['speed_y'] += (g * value['t'])
            value['t'] += 1

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()
            if not value['hit'] and value['x'] < current_position[0] < value['x'] + 60 and value['y'] < current_position[1] < value['y'] + 60:
                path = os.path.join(os.getcwd(), 'half_' + key + '.png')
                value['img'] = pygame.image.load(path)
                value['speed_x'] += 10
                score +=1
                score_text = font.render(str(score), True, black, white)
                value['hit'] = True

        else:
            generate_random_fruits(key)

    gameDisplay.blit(sword_cursor, pygame.mouse.get_pos())  # fungsi ini mengubah cursor menjadi pedang 

    pygame.display.update()
    clock.tick(fps)

    for event in pygame.event.get():
     if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
     if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            if data[fruit]['throw']:
                update_nyawa()








