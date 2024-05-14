#fungsi menambahkan library yang diperlukan
import pygame
import sys
import os
import time
import random


# Set up game (score, fps game, data buah)
pygame.init()
clock   = pygame.time.Clock()
nyawa   = 3
score   = 0
fps     = 13 
fruits  = ['jambu', 'jeruk', 'melon', "bomb"]
data    = {}


# Set up layar
width       = 800
height      = 600
white       = (255, 255, 255)
black       = (0, 0, 0)
gameDisplay = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Fruit Ninja")


# fungsi untuk menambahkan bahan bahan game
background_image    = pygame.image.load(os.path.join(os.getcwd(),'images/background.jpg'))  # Replace 'background.jpg' with your background image file
background_image    = pygame.transform.scale(background_image, (width, height))
sword_cursor        = pygame.image.load(os.path.join(os.getcwd(), 'images/sword.png'))  # Replace 'sword_cursor.png' with your sword cursor image file
sword_cursor        = pygame.transform.scale(sword_cursor, (50, 50))
font                = pygame.font.Font(os.path.join(os.getcwd(), 'images/comic.ttf'), 32)
score_text          = font.render(str(score), True, black, white)
lives_icon          = pygame.image.load('images/white_lives.png')


#inisialisasi backsound suara
pygame.mixer.init()
slash_sound     = pygame.mixer.Sound(os.path.join(os.getcwd(), 'images/sounds_FruitSlice.wav'))  # Ganti 'slash.wav' dengan file suara slash yang Anda miliki
# bomb_sound      = pygame.mixer.Sound(os.path.join(os.getcwd(), 'sounds/bomb_explosion.wav'))  # Ganti 'bomb_explosion.wav' dengan file suara ledakan bomb yang Anda miliki
backsound_game  = pygame.mixer.music.load(os.path.join(os.getcwd(), 'images/menu.mp3'))


# Fungsi untuk membuat random fruits
def generate_random_fruits(fruit):
    if fruit in "bomb":
       path = os.path.join(os.getcwd(), 'images/bomb.png')
    else:
       path = os.path.join(os.getcwd(),"images/" + fruit + '.png')
    data[fruit] = {
        'img': pygame.image.load(path),
        'x': random.randint(100, 500),
        'y': 800,
        'speed_x': random.randint(-10, 10),
        'speed_y': random.randint(-80, -50),#control kecepatan throw
        'throw': False,
        't': 0,
        'hit': False,
    }

    if random.random() >= 0.75:
        data[fruit]['throw'] = True
    else:
        data[fruit]['throw'] = False


# Dictionary to hold the data the random fruit generation
data = {}
for fruit in fruits:
    generate_random_fruits(fruit)

def hide_cross_lives(x, y):
    gameDisplay.blit(pygame.image.load("images/red_lives.png"), (x, y))


# Generic method to draw fonts on the screen
font_name = pygame.font.match_font('comic.ttf')
def draw_text(display, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    gameDisplay.blit(text_surface, text_rect)


# draw players lives
def draw_lives(display, x, y, lives, image) :
    for i in range(lives) :
        img = pygame.image.load(image)
        img_rect = img.get_rect()       #gets the (x,y) coordinates of the cross icons (lives on the the top rightmost side)
        img_rect.x = int(x + 35 * i)    #sets the next cross icon 35pixels awt from the previous one
        img_rect.y = y                  #takes care of how many pixels the cross icon should be positioned from top of the screen
        display.blit(img, img_rect)


# Generate initial random fruits
for fruit in fruits:
    generate_random_fruits(fruit)
pygame.mouse.set_visible(False)  # menyembunyikan bentuk cursor defaut
pygame.display.update()


# fungsi menampilkan logo "FRUIT" di menu awal
logo_image = pygame.image.load(os.path.join(os.getcwd(), 'images/logo.png'))  # udah 'fruit_ninja_logo.png' sesuai dengan format nama gambar
logo_image = pygame.transform.scale(logo_image, (300, 150))


def show_menu():
    gameDisplay.blit(background_image, (0,0))
    gameDisplay.blit(logo_image, (width // 2 - 150, height // 4))
    menu_text = font.render("KLIK SPACE UNTUK MEMULAI", True, white)
    gameDisplay.blit(menu_text, (width // 2.5 - 150, height // 1.5))
    if not game_over :
        draw_text(gameDisplay,"Score : " + str(score), 100 , width // 1.45 - 150, height // 7)
    pygame.display.flip() 
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
pygame.mixer.music.play(-1)
def play_slash_sound():
    pygame.mixer.Sound.play(slash_sound)




# fungsi utama game 
first_round = True
game_over = True        #terminates the game While loop if more than 3-Bombs are cut
game_running = True     #used to manage the game loop
while game_running :
    if game_over :
        if first_round :
            show_menu()
            first_round = False
        game_over = False
        player_lives = 3
        draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')
        score = 0

    for event in pygame.event.get():
        # checking for closing window
        if event.type == pygame.QUIT:
            game_running = False

    gameDisplay.blit(background_image, (0, 0))
    gameDisplay.blit(score_text, (0, 0))
    draw_lives(gameDisplay, 690, 5, player_lives, 'images/red_lives.png')

    for key, value in data.items():
        if value['throw']:
            value['x'] += value['speed_x']          #moving the fruits in x-coordinates
            value['y'] += value['speed_y']          #moving the fruits in y-coordinate
            value['speed_y'] += (1 * value['t'])    #increasing y-corrdinate
            value['t'] += 1                         #increasing speed_y for next loop

            if value['y'] <= 800:
                gameDisplay.blit(value['img'], (value['x'], value['y']))    #displaying the fruit inside screen dynamically
            else:
                generate_random_fruits(key)

            current_position = pygame.mouse.get_pos()   #gets the current coordinate (x, y) in pixels of the mouse

            if not value['hit'] and current_position[0] > value['x'] and current_position[0] < value['x']+60 \
                    and current_position[1] > value['y'] and current_position[1] < value['y']+60:
                if key == 'bomb':
                    player_lives -= 1
                    if player_lives == 0:
                        hide_cross_lives(690, 15)
                    elif player_lives == 1 :
                        hide_cross_lives(725, 15)
                    elif player_lives == 2 :
                        hide_cross_lives(760, 15)   
                        



                    #if the user clicks bombs for three time, GAME OVER message should be displayed and the window should be reset
                    if player_lives < 0 :
                        show_menu()
                        game_over = True
                    half_fruit_path = "images/ledakan.png"
                    #sound ledakan bomb
                else:
                    half_fruit_path = "images/half_" + key + ".png"
                    play_slash_sound()

                value['img'] = pygame.image.load(half_fruit_path)
                value['speed_x'] += 10
                if key != 'bomb' :
                    score += 1
                score_text = font.render('Score : ' + str(score), True, (255, 255, 255))
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









