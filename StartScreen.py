# These imports allow for the font, access to the main function, and graphical/gameplay interface.
import Chess
import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions and settings
width, height = 1000, 800
SQUARE_SIZE = 800 // 8
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Game')

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
grey = (200, 200, 200)
dgreen = (107, 142, 35)

# Fonts
chess_font = pygame.font.SysFont(None, 300)
players_font = pygame.font.SysFont(None, 100)
message_font = pygame.font.SysFont(None, 30)

# Button text
buttons = ['Chess', '1 player', '2 players', 'Rules']  # Added 'Rules' button

# Sound
pygame.mixer.music.load('Sounds/Calming Jazz to Play Chess.mp3')
pygame.mixer.music.play(-1)

# This fucntion creates the button imaged on the start screen, the buttons will be used later.
def draw_buttons():
    button_list = []  # Empty list to store buttons
    for i, text in enumerate(buttons):
        if text == 'Chess':
            button_surf = chess_font.render(text, True, black, grey)
            button_rect = button_surf.get_rect(center=((width - 200) // 2, 150))
        elif text == 'Rules':  # For the 'Rules' button
            button_surf = players_font.render(text, True, black, grey)
            button_rect = button_surf.get_rect(center=((width - 200) // 2, 650))  # Adjusted position
        else:
            button_surf = players_font.render(text, True, black, grey)
            if text == '1 player':
                button_rect = button_surf.get_rect(center=((width - 200) // 2, 450))
            elif text == '2 players':
                button_rect = button_surf.get_rect(center=((width - 200) // 2, 550))
        screen.blit(button_surf, button_rect)
        button_list.append((button_rect, text))
    return button_list

# This show message, uses the font from the top of the file, to create and render a small line of code at the top of the start screen.
def show_message(message):
    msg_surf = message_font.render(message, True, black, grey)
    msg_rect = msg_surf.get_rect(center=((width - 200) // 2, 300))
    screen.blit(msg_surf, msg_rect)
    pygame.display.flip()
    pygame.time.wait(5000)

# This function is the same only moved down 30 pixels as that is how vertically wide the characters are.
def show_message2(message):
    msg_surf = message_font.render(message, True, black, grey)
    msg_rect = msg_surf.get_rect(center=((width - 200) // 2, 330))
    screen.blit(msg_surf, msg_rect)
    pygame.display.flip()
    pygame.time.wait(5000)

# Same here another 30 pixels down.
def show_message3(message):
    msg_surf = message_font.render(message, True, black, grey)
    msg_rect = msg_surf.get_rect(center=((width - 200) // 2, 360))
    screen.blit(msg_surf, msg_rect)
    pygame.display.flip()
    pygame.time.wait(5000)

# Last one, another 30 down, this allows us to have four messages on the screen at once using the same style/sizing but preventing overlap.
def show_message4(message):
    msg_surf = message_font.render(message, True, black, grey)
    msg_rect = msg_surf.get_rect(center=((width - 200) // 2, 390))
    screen.blit(msg_surf, msg_rect)
    pygame.display.flip()
    pygame.time.wait(5000)

""" This is the main function that creates the screen and the black rectangle on the right side that has the timer on it.
It calls the functions defined above allows the user to click on the buttons, the buttons call the main chess file and tell it if the user 
is playing single or 2-player """

"""
def show_main():
    # Game loop
    running = True
    while running:
        screen.fill(grey)
        # Draws the squares of the board
        for row in range(8):
            for col in range(8):
                square_color = dgreen if (row + col) % 2 == 0 else grey
                pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        pygame.draw.rect(screen, (0, 0, 0), (800, 0, 200, 800))  # Right black rectangle
        
        button_list = draw_buttons()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button_rect, text in button_list:
                    if button_rect.collidepoint(event.pos):
                        if text == 'Chess':
                            pass  # This could be a placeholder for another function or feature
                        elif text == '1 player':
                            Chess.chess_main(single_player=True)
                        elif text == '2 players':
                            Chess.chess_main(single_player=False)
                        elif text == 'Rules':  
                            show_message('You have one minute to make a move.')
                            show_message2('The game shows possible moves each piece can make when you click it.')
                            show_message3('The highlighted piece was the last moved.')
                            show_message4('One player is against a chess-bot, enjoy!')             
                                       

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    show_main()
