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
players_font = pygame.font.SysFont(None,100)
message_font = pygame.font.SysFont(None,30)

# Button text
buttons = ['Chess', '1 player', '2 players']

# Sound
pygame.mixer.music.load('Sounds/Calming Jazz to Play Chess.mp3')
pygame.mixer.music.play(-1)

def draw_buttons(): 
    button_list = [] #empty list to store
    for i, text in enumerate(buttons): #goes down the list - keeping track 
        if text == 'Chess':
            button_surf = chess_font.render(text, True, black, grey) #renders text onto surface using chess_font
            button_rect = button_surf.get_rect(center=((width - 200) // 2, 150))  # Adjusted position for "Chess" - makes rectange around
        else:
            button_surf = players_font.render(text, True, black, grey) #renders using player font
            if text == '1 player':
                button_rect = button_surf.get_rect(center=((width - 200) // 2, 450))  # Centered position for "1 player" rectange creation
            elif text == '2 players':
                button_rect = button_surf.get_rect(center=((width - 200) // 2, 550))  # Lower position for "2 players" rectangle creation
        
        screen.blit(button_surf, button_rect) #update/draw screen essentially
        button_list.append((button_rect, text)) #adds to list
    return button_list #returning with each button and text


def show_message(message):
    msg_surf = message_font.render(message, True, black, grey) #using message font
    msg_rect = msg_surf.get_rect(center=((width - 200) // 2, 300)) #rectangle button
    screen.blit(msg_surf, msg_rect) #blit creates at given location
    pygame.display.flip() #supdate display
    pygame.time.wait(3000)  # Display the message for 2 seconds

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
        pygame.draw.rect(screen, (0, 0, 0), (800, 0, 200, 800)) #right black rectangle
        
        button_list = draw_buttons() #calls buttons
        pygame.display.flip() #updates to display everything
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #if its a quitting window
                pygame.quit() #quit 
                sys.exit() #end program
            elif event.type == pygame.MOUSEBUTTONDOWN: #check if mouse is pressed 
                for button_rect, text in button_list: #loop over rectangle in button list from above
                    if button_rect.collidepoint(event.pos): #if it overlaps on defined area - essentially clicking
                        if text == 'Chess':
                            pass # Call your chess main function
                        elif text == '1 player':
                            Chess.one_player_chess_main()
                        elif text == '2 players':
                            Chess.chess_main()  # Or a different function for 2 players

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    show_main()