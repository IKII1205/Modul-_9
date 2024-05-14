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
                score += 1
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
