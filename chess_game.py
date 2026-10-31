import pygame
import chess

# -----------------------------
# SETTINGS
# -----------------------------

WIDTH = 640
HEIGHT = 640
SQUARE_SIZE = WIDTH // 8

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Chess Game")

clock = pygame.time.Clock()

# Colors
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
HIGHLIGHT = (246, 246, 105)
MOVE_COLOR = (100, 180, 100)

# Chess pieces
pieces = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",

    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚"
}

font = pygame.font.SysFont("segoeuisymbol", 60)


# -----------------------------
# DRAW BOARD
# -----------------------------

def draw_board(board, selected_square=None, legal_moves=None):

    screen.fill((0, 0, 0))

    for row in range(8):
        for col in range(8):

            # Calculate square color
            if (row + col) % 2 == 0:
                color = LIGHT
            else:
                color = DARK

            x = col * SQUARE_SIZE
            y = row * SQUARE_SIZE

            pygame.draw.rect(
                screen,
                color,
                (x, y, SQUARE_SIZE, SQUARE_SIZE)
            )

            # Highlight selected square
            square = chess.square(col, 7 - row)

            if square == selected_square:
                pygame.draw.rect(
                    screen,
                    HIGHLIGHT,
                    (x, y, SQUARE_SIZE, SQUARE_SIZE)
                )

            # Highlight legal destinations
            if legal_moves and square in legal_moves:

                center_x = x + SQUARE_SIZE // 2
                center_y = y + SQUARE_SIZE // 2

                pygame.draw.circle(
                    screen,
                    MOVE_COLOR,
                    (center_x, center_y),
                    12
                )

            # Draw piece
            piece = board.piece_at(square)

            if piece:

                symbol = pieces[piece.symbol()]

                text = font.render(
                    symbol,
                    True,
                    (20, 20, 20)
                )

                text_rect = text.get_rect(
                    center=(
                        x + SQUARE_SIZE // 2,
                        y + SQUARE_SIZE // 2
                    )
                )

                screen.blit(text, text_rect)


# -----------------------------
# GET SQUARE FROM MOUSE
# -----------------------------

def get_square_from_mouse(position):

    x, y = position

    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    if col < 0 or col > 7 or row < 0 or row > 7:
        return None

    return chess.square(col, 7 - row)


# -----------------------------
# SHOW GAME STATUS
# -----------------------------

def show_status(board):

    if board.is_checkmate():

        winner = "Black" if board.turn == chess.WHITE else "White"

        print("CHECKMATE!")
        print(winner, "wins!")

        return True

    if board.is_stalemate():

        print("STALEMATE!")
        return True

    if board.is_insufficient_material():

        print("DRAW - Insufficient material!")
        return True

    if board.is_check():

        print("CHECK!")

    return False


# -----------------------------
# MAIN GAME
# -----------------------------

def main():

    board = chess.Board()

    selected_square = None
    legal_moves = []

    running = True
    game_over = False

    while running:

        for event in pygame.event.get():

            # Close window
            if event.type == pygame.QUIT:
                running = False

            # Mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:

                if game_over:
                    continue

                square = get_square_from_mouse(
                    pygame.mouse.get_pos()
                )

                if square is None:
                    continue

                # --------------------------------
                # SELECT A PIECE
                # --------------------------------

                if selected_square is None:

                    piece = board.piece_at(square)

                    # Make sure there is a piece
                    # belonging to the current player
                    if piece and piece.color == board.turn:

                        selected_square = square

                        legal_moves = [
                            move.to_square
                            for move in board.legal_moves
                            if move.from_square == selected_square
                        ]

                # --------------------------------
                # MOVE PIECE
                # --------------------------------

                else:

                    move = chess.Move(
                        selected_square,
                        square
                    )

                    # Promotion
                    if (
                        board.piece_at(selected_square)
                        and board.piece_at(selected_square).piece_type
                        == chess.PAWN
                        and chess.square_rank(square) in [0, 7]
                    ):

                        move = chess.Move(
                            selected_square,
                            square,
                            promotion=chess.QUEEN
                        )

                    # Check whether move is legal
                    if move in board.legal_moves:

                        board.push(move)

                        print(
                            "Move:",
                            board.peek()
                        )

                        game_over = show_status(board)

                        selected_square = None
                        legal_moves = []

                    else:

                        # If player clicked another
                        # friendly piece, select it
                        piece = board.piece_at(square)

                        if piece and piece.color == board.turn:

                            selected_square = square

                            legal_moves = [
                                move.to_square
                                for move in board.legal_moves
                                if move.from_square == selected_square
                            ]

                        else:

                            selected_square = None
                            legal_moves = []

        # Draw everything
        draw_board(
            board,
            selected_square,
            legal_moves
        )

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


# -----------------------------
# START GAME
# -----------------------------

if __name__ == "__main__":
    main()