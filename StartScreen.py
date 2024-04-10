from Chess import chess_main
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
players_font = pygame.font.SysFont(None,100)
message_font = pygame.font.SysFont(None,30)

# Button text
buttons = ['Chess', '1 player', '2 players']

def draw_buttons():
    button_list = []
    for i, text in enumerate(buttons):
        if text == 'Chess':
            button_surf = chess_font.render(text, True, black, grey)
            button_rect = button_surf.get_rect(center=((width - 200) // 2, 150))  # Adjusted position for "Chess"
        else:
            button_surf = players_font.render(text, True, black, grey)
            if text == '1 player':
                button_rect = button_surf.get_rect(center=((width - 200) // 2, 450))  # Centered position for "1 player"
            elif text == '2 players':
                button_rect = button_surf.get_rect(center=((width - 200) // 2, 550))  # Lower position for "2 players"
        
        screen.blit(button_surf, button_rect)
        button_list.append((button_rect, text))
    return button_list


def show_message(message):
    msg_surf = message_font.render(message, True, black, grey)
    msg_rect = msg_surf.get_rect(center=((width - 200) // 2, 300))
    screen.blit(msg_surf, msg_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Display the message for 2 seconds

# Game loop
running = True
while running:
    screen.fill(grey)
    # Draws the squares of the board
    for row in range(8):
        for col in range(8):
            square_color = dgreen if (row + col) % 2 == 0 else grey
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (800, 0, 200, 800))
    
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
                        chess_main()  # Call your chess main function
                    elif text == '1 player':
                        show_message("Pfft, you really think we have learned enough to code a Chess AI algorithm???")
                    elif text == '2 players':
                        chess_main()  # Or a different function for 2 players

# Quit Pygame
pygame.quit()
