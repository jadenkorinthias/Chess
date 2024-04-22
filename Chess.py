#Code was debugged with GPT-4 and Original work by Andrew, Jaden, and Kyle
#Contributions: Andrew: Main loop and Functions
#               Jaden: Start Screen
#               Kyle: Board, Pieces, and Functions

import pygame
import base64
import StartScreen
import random

#sound setup
capture = pygame.mixer.music.load("Sounds/capture.mp3")

# Constants for window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
SQUARE_SIZE = 800 // 8  # Assumes a square window for a square chess board
LGRAY = (211, 211, 211)  # Light gray squares
DGREEN = (107, 142, 35)  # Dark green squares
YELLOW = (255, 255, 0)  # Yellow
WHITE = (255, 255, 255) # White
FPS = 60

#Icons from www.flaticon.com
PIECES = {
    "b_bishop": pygame.image.load("icons/b_bishop.png"),
    "b_king": pygame.image.load("icons/b_king.png"),
    "b_knight": pygame.image.load("icons/b_knight.png"),
    "b_pawn": pygame.image.load("icons/b_pawn.png"),
    "b_queen": pygame.image.load("icons/b_queen.png"),
    "b_rook": pygame.image.load("icons/b_rook.png"),
    "w_bishop": pygame.image.load("icons/w_bishop.png"),
    "w_king": pygame.image.load("icons/w_king.png"),
    "w_knight": pygame.image.load("icons/w_knight.png"),
    "w_pawn": pygame.image.load("icons/w_pawn.png"),
    "w_queen": pygame.image.load("icons/w_queen.png"),
    "w_rook": pygame.image.load("icons/w_rook.png"),
}

#init pygame
pygame.init()

# Chessboard class
class ChessBoard:
    def __init__(self):
        self.board = [[None for row in range(8)] for col in range(8)]
        self.initialize_pieces()
        self.last_move_end = None # Store position of the end of the last move

    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]
    
    def __setitem__(self, position, value):
        x, y = position
        self.board[x][y] = value

    def initialize_pieces(self):
        # Initialize black pieces
        self.board[0][0] = Rook('black', (0, 0))
        self.board[0][1] = Knight('black', (0, 1))
        self.board[0][2] = Bishop('black', (0, 2))
        self.board[0][3] = Queen('black', (0, 3))
        self.board[0][4] = King('black', (0, 4))
        self.board[0][5] = Bishop('black', (0, 5))
        self.board[0][6] = Knight('black', (0, 6))
        self.board[0][7] = Rook('black', (0, 7))
        for row in range(8):
            self.board[1][row] = Pawn('black', (1, row))

        # Initialize white pieces
        self.board[7][0] = Rook('white', (7, 0))
        self.board[7][1] = Knight('white', (7, 1))
        self.board[7][2] = Bishop('white', (7, 2))
        self.board[7][3] = Queen('white', (7, 3))
        self.board[7][4] = King('white', (7, 4))
        self.board[7][5] = Bishop('white', (7, 5))
        self.board[7][6] = Knight('white', (7, 6))
        self.board[7][7] = Rook('white', (7, 7))
        for row in range(8):
            self.board[6][row] = Pawn('white', (6, row))

    def move_piece(self, piece, new_position):
        old_x, old_y = piece.position  # Get the current position of the piece
        new_x, new_y = new_position    # Get the new position where the piece will be moved
        self.board[old_x][old_y] = None  # Remove the piece from its old position by setting that cell to None
        # Place the piece at its new position on the board
        # If there was another piece at this position, it is 'captured' by being overwritten and thus removed from the board
        self.board[new_x][new_y] = piece  
        piece.position = new_position  # Update the piece's position attribute to reflect its new location

        self.last_move_end = (new_y, new_x) # Record the end position of the last move

        # If the moved piece is a pawn and this is its first move, set its 'first_move' attribute to False
        if isinstance(piece, Pawn):
            piece.first_move = False  

    # Pawn Promotion method
    def promote_pawn(self, piece, new_position):
        new_x, new_y = new_position
        # Check if the pawn has reached the promotion condition
        if isinstance(piece, Pawn):
            if (piece.color == 'white' and new_x == 0) or (piece.color == 'black' and new_x == 7):
                self.board[new_x][new_y] = Queen(piece.color, new_position)

    def is_in_check(self, king_color):
        # Find the king's position
        king_position = None
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == king_color:
                    king_position = piece.position
                    break

        # Check if any opposing pieces can attack the king
        for row in self.board:
            for piece in row:
                if piece and piece.color != king_color:
                    if king_position in piece.available_moves(self):
                        return True
        return False

    def is_checkmate(self, king_color):
        if not self.is_in_check(king_color):
            return False

        # Check if any move can get the king out of check
        for row in self.board:
            for piece in row:
                if piece and piece.color == king_color:
                    original_position = piece.position
                    for move in piece.available_moves(self):
                        # Save the target piece before the simulated move
                        target_piece = self.board[move[0]][move[1]]
                        # Simulate the move
                        self.move_piece(piece, move)
                        if not self.is_in_check(king_color):
                            # Undo the move
                            self.move_piece(piece, original_position)
                            self.board[move[0]][move[1]] = target_piece  # Restore the target piece
                            return False
                        # Undo the move
                        self.move_piece(piece, original_position)
                        self.board[move[0]][move[1]] = target_piece  # Restore the target piece
        return True

    def is_king_present(self, color):
        """Check if the king of the given color is present on the board."""
        return any(isinstance(piece, King) and piece.color == color for row in self.board for piece in row)


# Base class for all chess pieces
class ChessPiece:
    def __init__(self, color, position):
        self.color = color
        self.position = position

    def available_moves(self, board):
        # This will be overridden by each specific piece type
        raise NotImplementedError("This method should be implemented by subclasses")

# Pawn piece
class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.first_move = True  # Pawns have a different move if it's their first

    def available_moves(self, board):
        moves = []
        x, y = self.position
        direction = -1 if self.color == 'white' else 1  # Adjusted to use integers for direction

        # Check for a standard forward move in chess for a pawn.
        if 0 <= x + direction < 8 and board[x + direction, y] is None:  # Check if the cell directly in front is within bounds and empty
            moves.append((x + direction, y))  # Add this move to the list of possible moves
            # Check if a two-square forward move is allowed (typically used on the pawn's first move)
            if self.first_move and board[x + 2 * direction, y] is None:
                moves.append((x + 2 * direction, y))  # Add the two-square move to the list of possible moves

        # Iterate over possible capture moves, which occur diagonally
        for dy in [-1, 1]:  # Loop to check both left and right diagonal moves
            # Ensure the diagonal cell is within the bounds of the board
            if 0 <= y + dy < 8 and 0 <= x + direction < 8:
                # Check if the diagonal cell is occupied by an opponent's piece
                if board[x + direction, y + dy] is not None and board[x + direction, y + dy].color != self.color:
                    moves.append((x + direction, y + dy))  # Add the capture move to the list of possible moves
        return moves

# Define the Rook piece, inheriting from the ChessPiece base class
class Rook(ChessPiece):
    # Constructor to initialize a Rook object with a color and its initial position
    def __init__(self, color, position):
        super().__init__(color, position)  # Call the constructor of the superclass (ChessPiece) to set color and position

    # Method to calculate all available moves for the Rook piece from its current position
    def available_moves(self, board):
        moves = []  # Initialize an empty list to store all valid moves
        x, y = self.position  # Get the current x, y coordinates of the Rook

        # Define the four possible directions in which a Rook can move: up, right, down, left
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # Loop over each direction the Rook can move
        for dx, dy in directions:
            # Attempt to move in this direction up to 7 squares (maximum possible on a chessboard)
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i  # Calculate the new position based on direction and distance i

                # Check if the new position is within the bounds of the chessboard
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # If the target square is empty, the move is valid
                    if board[new_x, new_y] is None:
                        moves.append((new_x, new_y))  # Add this move to the list of valid moves
                    # If the target square is occupied by an opponent's piece, the move is valid and captures that piece
                    elif board[new_x, new_y].color != self.color:
                        moves.append((new_x, new_y))  # Add the capturing move to the list
                        break  # Stop checking further in this direction since the Rook cannot jump over pieces
                    else:
                        break  # If the square is occupied by a piece of the same color, stop checking this direction

        return moves  # Return the list of all valid moves

# Define the Knight piece, inheriting from the ChessPiece base class
class Knight(ChessPiece):
    # Constructor to initialize a Knight object with a color and its initial position
    def __init__(self, color, position):
        super().__init__(color, position)  # Call the constructor of the superclass (ChessPiece) to set color and position

    # Method to calculate all available moves for the Knight piece from its current position
    def available_moves(self, board):
        moves = []  # Initialize an empty list to store all valid moves
        x, y = self.position  # Get the current x, y coordinates of the Knight

        # Define all possible 'L' shaped moves a Knight can make
        potential_moves = [
            (x + 2, y + 1), (x + 2, y - 1),  # Moves that go two squares horizontally and one square vertically
            (x - 2, y + 1), (x - 2, y - 1),  # Moves that go two squares horizontally and one square vertically in the opposite direction
            (x + 1, y + 2), (x + 1, y - 2),  # Moves that go one square horizontally and two squares vertically
            (x - 1, y + 2), (x - 1, y - 2),  # Moves that go one square horizontally and two squares vertically in the opposite direction
        ]

        # Iterate over all potential moves
        for new_x, new_y in potential_moves:
            # Check if the new position is within the bounds of the chess board
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                # Check if the target square is either empty or occupied by an opponent's piece
                if board[new_x, new_y] is None or board[new_x, new_y].color != self.color:
                    moves.append((new_x, new_y))  # Add the move to the list of valid moves if the square is valid for movement

        return moves  # Return the list of all valid moves


# Define the Bishop class, which inherits from the ChessPiece base class
class Bishop(ChessPiece):
    # Constructor to initialize a Bishop object with its color and starting position
    def __init__(self, color, position):
        super().__init__(color, position)  # Call the superclass constructor to set the color and position attributes

    # Method to determine all available moves for the Bishop from its current position
    def available_moves(self, board):
        moves = []  # Initialize an empty list to store potential moves
        x, y = self.position  # Retrieve the current position of the Bishop on the board

        # Define the four diagonal directions in which a Bishop can move
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        # Iterate over each direction to explore potential moves
        for dx, dy in directions:
            # Attempt to move in this direction for up to 7 squares (the maximum on a chess board)
            for step in range(1, 8):
                new_x = x + dx * step  # Calculate the new x-coordinate based on the direction and step distance
                new_y = y + dy * step  # Calculate the new y-coordinate similarly

                # Check if the new coordinates are still within the bounds of the board
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Check if the target square is empty
                    if board[new_x, new_y] is None:
                        moves.append((new_x, new_y))  # If so, it's a valid move and is added to the moves list
                    else:
                        # If the target square is not empty and contains a piece of a different color
                        if board[new_x, new_y].color != self.color:
                            moves.append((new_x, new_y))  # It's a valid capture move, add to the list
                        break  # Bishop cannot jump over other pieces, so stop checking further along this direction
                else:
                    break  # If out of bounds, stop checking this direction and move to the next

        return moves  # Return the list of all valid moves determined


# Define the Queen class, which inherits from the ChessPiece base class
class Queen(ChessPiece):
    # Constructor to initialize a Queen object with its color and starting position
    def __init__(self, color, position):
        super().__init__(color, position)  # Call the superclass constructor to set the color and position attributes

    # Method to determine all available moves for the Queen from its current position
    def available_moves(self, board):
        moves = []  # Initialize an empty list to store potential moves
        x, y = self.position  # Retrieve the current position of the Queen on the board

        # Define the eight possible directions in which a Queen can move: includes horizontal, vertical, and diagonal directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  # Directions for horizontal and vertical movement
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Directions for diagonal movement

        # Iterate over each direction to explore potential moves
        for dx, dy in directions:
            # Attempt to move in this direction for up to 7 squares (the maximum on a chess board)
            for step in range(1, 8):
                new_x = x + dx * step  # Calculate the new x-coordinate based on the direction and step distance
                new_y = y + dy * step  # Calculate the new y-coordinate similarly

                # Check if the new coordinates are still within the bounds of the board
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Check if the target square is empty
                    if board[new_x, new_y] is None:
                        moves.append((new_x, new_y))  # If so, it's a valid move and is added to the moves list
                    else:
                        # If the target square is not empty and contains a piece of a different color
                        if board[new_x, new_y].color != self.color:
                            moves.append((new_x, new_y))  # It's a valid capture move, add to the list
                        break  # Queen cannot jump over other pieces, so stop checking further along this direction
                else:
                    break  # If out of bounds, stop checking this direction and move to the next

        return moves  # Return the list of all valid moves determined


# Define the King class, which inherits from the ChessPiece base class
class King(ChessPiece):
    # Constructor to initialize a King object with its color and starting position
    def __init__(self, color, position):
        super().__init__(color, position)  # Call the superclass constructor to set the color and position attributes

    # Method to determine all available moves for the King from its current position
    def available_moves(self, board):
        moves = []  # Initialize an empty list to store potential moves
        x, y = self.position  # Retrieve the current position of the King on the board

        # Define the eight possible directions in which a King can move: includes one square in every possible direction
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  # Directions for horizontal and vertical movement
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Directions for diagonal movement

        # Iterate over each direction to explore potential moves
        for dx, dy in directions:
            new_x = x + dx  # Calculate the new x-coordinate based on the direction
            new_y = y + dy  # Calculate the new y-coordinate similarly

            # Check if the new coordinates are still within the bounds of the board
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                # Check if the target square is either empty or occupied by an opponent's piece
                if board[new_x, new_y] is None or board[new_x, new_y].color != self.color:
                    moves.append((new_x, new_y))  # If so, it's a valid move and is added to the moves list

        return moves  # Return the list of all valid moves determined


def draw_board(screen, board_obj):
    # Draws the squares of the board
    for row in range(8):
        for col in range(8):
            square_color = LGRAY if (row + col) % 2 == 0 else DGREEN
            if (col, row) == board_obj.last_move_end:
                square_color = YELLOW  # Highlight color
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.rect(screen, (0, 0, 0), (800, 0, 200, 800))

def draw_pieces(screen, board_obj):
    piece_size = (80, 80)  # Size of the piece images
    piece_offset = (SQUARE_SIZE - piece_size[0]) // 2

    # Iterate over each square and draw the pieces
    for row in range(8):
        for col in range(8):
            piece = board_obj[row, col]  # Access the piece at (row, col)
            if piece:
                piece_key = f"{piece.color[0]}_{type(piece).__name__.lower()}"
                piece_image = PIECES[piece_key]
                piece_image = pygame.transform.scale(piece_image, piece_size)
                # Calculate the position to place the piece image
                piece_position = (col * SQUARE_SIZE + piece_offset, row * SQUARE_SIZE + piece_offset)
                screen.blit(piece_image, piece_position)

def highlight_selected_piece(screen, selected_pos):
    # Highlights the selected piece
    if selected_pos:
        y , x = selected_pos
        pygame.draw.rect(screen, YELLOW, (x * SQUARE_SIZE, (y) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def display_valid_moves(screen, moves):
    # Use one surface with transparency for all circles
    circle_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    circle_color = (128, 128, 128, 128)  # Semi-transparent gray

    for row, col in moves:
        circle_surface.fill((0, 0, 0, 0))  # Clear previous circle
        circle_position = (SQUARE_SIZE // 2, SQUARE_SIZE // 2)
        pygame.draw.circle(circle_surface, circle_color, circle_position, 15)
        screen.blit(circle_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def if_castle(king, board): #WIP Kyle
    # Ensure the piece is a King and it has not moved
    if isinstance(king, King) and not king.has_moved:
        # Determine the row for castling based on the king's color
        row = 0 if king.color == 'white' else 7

        # Get the pieces in the king's row
        row_pieces = board.board[row]
        
        king_pos = king.position[1] # Column index of the king
        rook_positions = [0,7] # Rooks should be at columns 0 and 7

        for pos in rook_positions:
            rook = row_pieces[pos]
            # Ensure there's a Rook at the position and it has not moved
            if isinstance(rook,Rook) and not rook.has_moved:
                 # Calculate the direction to check for clear path
                step = 1 if pos > king_pos else -1
                # Check if the squares between the king and the rook are empty
                clear_path = all(row_pieces[king_pos + i * step] is None for i in range(1,abs(pos-king_pos)))
                 # Check if there is a clear path and the king is not in check
                if clear_path and not board.is_in_check(king.color):
                    return True # Return True if castling is possible
    return False # Return False if castling is not possible

def draw_castle_moves(screen, moves): #WIP Kyle
    pass
    for move in moves:
        x, y = (move)
        pygame.draw.circle(screen, YELLOW, (x, y), pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA))

def get_piece_value(piece): #values from wikipedia - worth of each piece
    if isinstance(piece, Pawn):
        return 1
    elif isinstance(piece, Knight):
        return 3
    elif isinstance(piece, Bishop):
        return 3
    elif isinstance(piece, Rook):
        return 5
    elif isinstance(piece, Queen):
        return 9
    elif isinstance(piece, King):
        return 200

# Bot move logic
def bot_move(board):
    game_over = False
    all_moves = [] #empty list to store

    for row in range(8):
        for col in range(8):
            piece = board[(row, col)] #piece
            if piece and piece.color == 'black':  # Ensure we're only moving black pieces
                moves = piece.available_moves(board) #All availible moves based on piece and location
                for move in moves:
                    score = 0 #keep track of a moves value
                    target_x, target_y = move #location of move
                    captured_piece = board[(target_x, target_y)]  # Capture the piece if there is one
                    original_piece = board[(row, col)] #move location
                    board[(row, col)] = None
                    board[(target_x, target_y)] = piece
                    original_position = piece.position
                    piece.position = (target_x, target_y) #stores
                    
                    if not board.is_in_check('black'): #make sure the move does not put black king in check
                        if captured_piece:
                            score += get_piece_value(captured_piece)  # Value of captured piece
                        if 2 <= target_x <= 5 and 2 <= target_y <= 5:
                            score += 4  # Central squares are more valuable
                    else:
                        score -= 100  # Penalize moves that put king in check

                    board[(row, col)] = original_piece
                    board[(target_x, target_y)] = captured_piece
                    piece.position = original_position
                    
                    all_moves.append((piece, move, score)) #each potential move, which piece is moved and score value

    if all_moves:
            piece, best_move, _ = max(all_moves, key=lambda x: x[2])
            # Make the actual move
            board.move_piece(piece, best_move)
            opponent_color = 'white'  # Assuming black is the bot
            # Check if the move resulted in a check or a checkmate
            in_check = board.is_in_check(opponent_color)
            king_present = board.is_king_present(opponent_color)

            # Print statements to debug or to log the game state
            if not king_present:
                print("King captured!")
                return game_over == True
            elif in_check:
                print("Check!")        
            return True
    return False  # No valid moves were available

# Pygame setup for the graphical interface
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.flip() #updates to display everything
pygame.display.set_caption('Chess Game')

# Andrew: chess_main function
# The chess_main function orchestrates the main gameplay loop for a chess game.
# It supports single-player (against a bot) and two-player modes, which are determined by the `single_player` flag.
# The function initializes the game board, clock, and other essential game elements such as pieces, their positions, and valid moves.
# Players alternate turns, starting with white. Each turn allows the player to select and move pieces according to chess rules.
# The function also supports the timer for each player, with the game transitioning turns automatically if a player's timer runs out of time.
# If the game ends, the game displays the status and prompts the user with options to play again, exit to the menu, or quit, using mouse clicks.
# The function continuously updates the display and checks for game-ending conditions, updating the status and handling the user's game decisions.

def chess_main(single_player=False):

    # Initliaized variables required for the game start state
    board = ChessBoard()
    clock = pygame.time.Clock()
    selected_piece = None
    selected_pos = None
    valid_moves = []
    castle_moves = []  # Initialized here to ensure it is available at the start
    current_turn = 'white'
    game_status = ""
    bot_active = single_player
    game_over = False
    #Timer setup
    initial_timer = 0 
    timers = {'white': initial_timer, 'black': initial_timer}

    #Initialize current_timer for the starting turn
    current_timer = timers[current_turn]

    # Interface buttons: play again, quit, or menu
    play_again_rect = pygame.Rect(830, 650, 200, 50)
    quit_rect = pygame.Rect(830, 700, 100, 50)
    menu_rect = pygame.Rect(830, 750, 200, 50)
    
    #Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    if play_again_rect.collidepoint(event.pos):
                        chess_main(single_player=single_player)
                        continue
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        return
                    elif menu_rect.collidepoint(event.pos):
                        StartScreen.show_main()
                        continue

                # Basic logic handling for chess game
                if not game_over:
                    mouse_pos = event.pos
                    if mouse_pos[0] < 800:
                        col = mouse_pos[0] // SQUARE_SIZE
                        row = mouse_pos[1] // SQUARE_SIZE
                        if selected_piece and (row, col) in valid_moves:
                            board.move_piece(selected_piece, (row, col))
                            #After moving the piece and changing turns update the timer for the next player
                            pygame.mixer.music.load("Sounds/move-self.mp3")
                            pygame.mixer_music.play(0)
                            board.promote_pawn(selected_piece, (row, col)) # Invoking the pawn promotion function
                            current_timer = timers[current_turn]
                            # Check if the king is missing after the move

                            # Handle castling if the selected piece is a King and the move is a castling move
                            if isinstance(selected_piece,King) and (row, col) in castle_moves:
                                # Execute castling: move the corresponding rook
                                if col == 2:  # Long castle
                                    rook = board[(row, 0)]
                                    board.move_piece(rook, (row, 3))
                                elif col == 6:  # Short castle
                                    rook = board[(row, 7)]
                                    board.move_piece(rook, (row, 5))

                            # Reset selections after any move
                            selected_piece = None
                            valid_moves = []
                            castle_moves = []  # Reset after move

                            # Check if the king is missing after the move
                            if not board.is_king_present('white') or not board.is_king_present('black'):
                                game_status = "Game Over!"
                                game_over = True
                            else:
                                opponent_color = 'black' if current_turn == 'white' else 'white'
                                if board.is_in_check(opponent_color):
                                    if board.is_checkmate(opponent_color):
                                        game_status = "Checkmate"
                                        game_over = True
                                    else:
                                        game_status = "Check"
                                else:
                                    game_status = ""
                                
                                # Ensure turn changes only here after a move is made
                                current_turn = opponent_color
                                current_timer = timers[current_turn]  # Reset the timer for the new turn
                        else:
                            # New selection or deselection
                            selected_pos = (row, col)
                            selected_piece = board[selected_pos]
                            if selected_piece and selected_piece.color == current_turn:
                                valid_moves = selected_piece.available_moves(board)
                                if isinstance(selected_piece, King):
                                    #castle_moves = if_castle(selected_piece, board)  # Get castling moves
                                    valid_moves.extend(castle_moves)  # Add castling moves to valid moves
                            else:
                                selected_piece = None
                                valid_moves = []
                                castle_moves = []  # Clear previous castling moves if any

        if bot_active and current_turn == 'black':
                pygame.display.flip()  # Bot's turn logic outside the event loop
                if bot_move(board):
                    current_turn = 'white'
                if board.is_in_check('white'):
                    if board.is_checkmate('white'):
                        game_status = "Checkmate"
                        game_over = True
                    else:
                        game_status = "Check"
                else:
                    game_status = ""

        screen.fill(pygame.Color("white"))
        draw_board(screen, board)
        draw_pieces(screen, board)

        if selected_piece:
            highlight_selected_piece(screen, selected_pos)
            display_valid_moves(screen, valid_moves)

        font = pygame.font.SysFont(None, 36)
        turn_text = font.render(f"{current_turn.capitalize()}'s Turn", True, (WHITE))
        screen.blit(turn_text, (830, 50))

        #Timer update and display
        time_passed = (clock.tick(60) / 1000.0) * 1.95 #Time passed in seconds
        if not game_over and current_turn:
            current_timer += time_passed
            
            #TODO: Add in slider for time
            
            # Changing turns if the current player runs out of time
            if current_timer >= 60:
                if current_turn == "white":
                    current_turn = "black"
                else:
                    current_turn = "white"
                current_timer = 0
        minutes, seconds = divmod(int(current_timer), 60)
        timer_text = font.render(f"Timer: {minutes:02}:{seconds:02}", True, (WHITE))
        screen.blit(timer_text, (830, 150))

        if game_status:
            status_text = font.render(game_status, True, (255, 0, 0))
            screen.blit(status_text, (830, 100))

        if game_over:
            game_over_font = pygame.font.SysFont(None, 150)
            game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (100, 350))

            play_again_font = pygame.font.SysFont(None, 36)
            play_again_text = play_again_font.render("Play again?", True, (WHITE))
            quit_text = play_again_font.render("Quit", True, (WHITE))
            screen.blit(play_again_text, (830, 650))
            screen.blit(quit_text, (830,700))

            menu_screen_font = pygame.font.SysFont(None, 36)
            menu_screen_text = menu_screen_font.render("Menu", True, (255,255,255))
            screen.blit(menu_screen_text,(830,750))

        pygame.display.flip()
        clock.tick(FPS)
