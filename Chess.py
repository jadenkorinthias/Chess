'''
Things to do:
1. DONE, AND TESTED: Add in highlight when chess piece is clicked. Chess piece acts like the user is grabbing it an follows around the mouse while the user has the mouse button pressed down. When released it releases the chess piece where the user drops it and checks if it is a valid spot.
2. DONE, AND  TESTED: Valid spots. When a user clicks on a chess piece the program will add in small grey and slighly transparent circles 30 pixels wide that will show the user all of the valid moves that it can make.
3. DONE, ish: managing the overall game state
4. DONE: turn management
5. FRICK: checks/checkmates, This is insanely complicated for some reason!!!!
6. DONE: game-end scenarios.
7. DONE: start screen
8. Player move log, on right side.
'''

import pygame

# Constants for window dimensions
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
SQUARE_SIZE = 800 // 8  # Assumes a square window for a square chess board
LGRAY = (211, 211, 211)  # Light gray squares
DGREEN = (107, 142, 35)  # Dark green squares
highlight_color = (255, 255, 0)  # Yellow

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

    def __getitem__(self, pos):
        x, y = pos
        return self.board[x][y]

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
        # If the moved piece is a pawn and this is its first move, set its 'first_move' attribute to False
        if isinstance(piece, Pawn):
            piece.first_move = False  

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

# Rook piece
class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def available_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Four possible directions for Rook movement

        for dx, dy in directions:
            for i in range(1, 8):
                new_x, new_y = x + dx * i, y + dy * i
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if board[new_x, new_y] is None:
                        moves.append((new_x, new_y))
                    elif board[new_x, new_y].color != self.color:
                        moves.append((new_x, new_y))
                        break
                    else:
                        break

        return moves

# Knight piece
class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def available_moves(self, board):
        moves = []
        x, y = self.position

        # Potential moves considering the 'L' shape movement
        potential_moves = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2),
        ]

        for new_x, new_y in potential_moves:
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                # Use board[new_x, new_y] instead of board[new_x][new_y]
                if board[new_x, new_y] is None or board[new_x, new_y].color != self.color:
                    moves.append((new_x, new_y))

        return moves

# Bishop piece
class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def available_moves(self, board):
        moves = []
        x, y = self.position

        # Directions a Bishop can move: diagonally in 4 ways
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            for step in range(1, 8):  # A bishop can move up to 7 squares in one direction
                new_x = x + dx * step
                new_y = y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Use board[new_x, new_y] to access the cell
                    if board[new_x, new_y] is None:
                        moves.append((new_x, new_y))
                    else:
                        # If there's a piece of different color, it can be captured
                        if board[new_x, new_y].color != self.color:
                            moves.append((new_x, new_y))
                        break  # Can't jump over pieces
                else:
                    break  # Stop if off the board

        return moves

# Queen piece
class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def available_moves(self, board):
        moves = []
        x, y = self.position

        # Directions a Queen can move: horizontally, vertically, and diagonally (like Rook and Bishop combined)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  # Horizontally and vertically
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonally

        for dx, dy in directions:
            for step in range(1, 8):  # A queen can move up to 7 squares in any direction
                new_x = x + dx * step
                new_y = y + dy * step
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    # Use board[new_x, new_y] to access the cell
                    if board[new_x, new_y] is None:
                        moves.append((new_x, new_y))
                    else:
                        # If there's a piece of different color, it can be captured
                        if board[new_x, new_y].color != self.color:
                            moves.append((new_x, new_y))
                        break  # Stop if there's a piece in the way
                else:
                    break  # Stop if off the board

        return moves

# King piece
class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position)

    def available_moves(self, board):
        moves = []
        x, y = self.position

        # Directions a King can move: one square in any direction
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0),  # Horizontally and vertically
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]  # Diagonally

        for dx, dy in directions:
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                # Use board[new_x, new_y] to access the cell
                if board[new_x, new_y] is None or board[new_x, new_y].color != self.color:
                    moves.append((new_x, new_y))

        return moves

def draw_board(screen):
    # Draws the squares of the board
    for row in range(8):
        for col in range(8):
            square_color = DGREEN if (row + col) % 2 == 0 else LGRAY
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
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
        pygame.draw.rect(screen, highlight_color, (x * SQUARE_SIZE, (y) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def display_valid_moves(screen, moves):
    # Use one surface with transparency for all circles
    circle_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
    circle_color = (128, 128, 128, 128)  # Semi-transparent gray

    for row, col in moves:
        circle_surface.fill((0, 0, 0, 0))  # Clear previous circle
        circle_position = (SQUARE_SIZE // 2, SQUARE_SIZE // 2)
        pygame.draw.circle(circle_surface, circle_color, circle_position, 15)
        screen.blit(circle_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

# Pygame setup for the graphical interface
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Chess Game')

def chess_main():
    board = ChessBoard()
    clock = pygame.time.Clock()
    selected_piece = None
    selected_pos = None
    valid_moves = []
    current_turn = 'white'
    game_status = ""
    game_over = False

    #Timer setup for both players
    initial_timer = 300 #300 seconds = 5 minuites
    timers = {'white': initial_timer, 'black': initial_timer}

    #Initialize current_timer for the starting turn
    current_timer = timers[current_turn]

    play_again_rect = pygame.Rect(830, 650, 200, 50)
    quit_rect = pygame.Rect(830, 700, 100, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    if play_again_rect.collidepoint(event.pos):
                        chess_main()
                        continue
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        return

                if not game_over:
                    mouse_pos = event.pos
                    #Only update timer for current player's turn
                    elapsed_time = clock.tick(60) / 1000.0
                    timers[current_turn] -= elapsed_time
                    #If the timer runs out
                    if timers[current_turn] <= 0:
                        game_status = f"{current_turn.capitalize()} time's up!"
                        game_over = True
                        timers[current_turn] = 0 
                    if mouse_pos[0] < 800:
                        col = mouse_pos[0] // SQUARE_SIZE
                        row = mouse_pos[1] // SQUARE_SIZE
                        if selected_piece and (row, col) in valid_moves:
                            board.move_piece(selected_piece, (row, col))
                            #After moving the piece and changing turns update the timer for the next player
                            current_timer = timers[current_turn] 
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
                                current_turn = opponent_color
                            selected_piece = None
                            valid_moves = []
                        selected_pos = (row, col)
                        selected_piece = board[selected_pos]
                        if selected_piece and selected_piece.color == current_turn:
                            valid_moves = selected_piece.available_moves(board)
                        else:
                            selected_piece = None
                            valid_moves = []

        screen.fill(pygame.Color("white"))
        draw_board(screen)
        draw_pieces(screen, board)

        if selected_piece:
            highlight_selected_piece(screen, selected_pos)
            display_valid_moves(screen, valid_moves)

        font = pygame.font.SysFont(None, 36)
        turn_text = font.render(f"{current_turn.capitalize()}'s Turn", True, (255, 255, 255))
        screen.blit(turn_text, (830, 50))

        #Timer update and display
        time_passed = (clock.tick(60) / 1000.0) * 1.95 #Time passed in seconds
        if not game_over and current_turn:
            current_timer -= time_passed
            if current_timer <= 0:
                game_status = current_turn.capitalize() + " time's up!"
                game_over = True
                current_timer = 0
        minutes, seconds = divmod(int(current_timer), 60)
        timer_text = font.render(f"Timer: {minutes:02}:{seconds:02}", True, (255, 255, 255))
        screen.blit(timer_text, (830, 150))

        if game_status:
            status_text = font.render(game_status, True, (255, 0, 0))
            screen.blit(status_text, (830, 100))

        if game_over:
            game_over_font = pygame.font.SysFont(None, 150)
            game_over_text = game_over_font.render("Game Over!", True, (255, 0, 0))
            screen.blit(game_over_text, (100, 350))

            play_again_font = pygame.font.SysFont(None, 36)
            play_again_text = play_again_font.render("Play again?", True, (255, 255, 255))
            quit_text = play_again_font.render("Quit", True, (255, 255, 255))
            screen.blit(play_again_text, (830, 650))
            screen.blit(quit_text, (830,700))

        pygame.display.flip()
        clock.tick(60)