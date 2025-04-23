import pygame as p
import ChessEngine
from animations import (
    animateMoveKnight, animateMovePawn, animateMoveRook, animateMoveBishop, animatetransfer,animateCheckmate,animateStalemate
)
from move_history import MoveHistoryWindow
# Constants
MARGIN=20
WIDTH = HEIGHT = 650
INFO_WIDTH = 150
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
screen = p.display.set_mode((WIDTH+ MARGIN+INFO_WIDTH, HEIGHT+MARGIN))

def loadImages():
    """Load and scale images for chess pieces and animation effects."""
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(
            p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE)
        )

    fireball_frames = []
    for i in range(1, 61):
        fireball_img = p.transform.scale(
            p.image.load(f"16_sunburn_spritesheet/{i}_16_sunburn_spritesheet.png"),
            (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        fireball_frames.append(fireball_img)
    IMAGES['fireball_frames'] = fireball_frames

    boom_frames = []
    for i in range(1, 13):
        boom_img = p.transform.scale(
            p.image.load(f"03/{39+i}_03.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        boom_frames.append(boom_img)
    IMAGES['boom_frames'] = boom_frames

    slash_color1_frames = []
    for i in range(1, 10):
        slash_img = p.transform.scale(
            p.image.load(f"Frames/Slash_color1_frame{i}.png"), (SQ_SIZE * 3, SQ_SIZE * 3)
        )
        slash_color1_frames.append(slash_img)
    IMAGES['Slash_color1_frame1'] = slash_color1_frames

    p_boom_frames = []
    for i in range(256, 269):
        p_boom_img = p.transform.scale(
            p.image.load(f"p_smoke/{i}_Smoke.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        p_boom_frames.append(p_boom_img)
    IMAGES['p_boom_frames'] = p_boom_frames

    p_slash_color1_frames = []
    for i in range(1, 11):
        p_slash_img = p.transform.scale(
            p.image.load(f"p_Frames/warrior_skill1_frame{i}.png"), (SQ_SIZE * 3, SQ_SIZE * 3)
        )
        p_slash_color1_frames.append(p_slash_img)
    IMAGES['p_Slash_color1_frame1'] = p_slash_color1_frames

    frost_frames = []
    for i in range(1, 58):
        frost_img = p.transform.scale(
            p.image.load(f"frost/frost ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        frost_frames.append(frost_img)
    IMAGES['frost_frames'] = frost_frames

    frostleft_frames = []
    for i in range(1, 47):
        frostleft_img = p.transform.scale(
            p.image.load(f"frostleft/frostleft ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        frostleft_frames.append(frostleft_img)
    IMAGES['frostleft_frames'] = frostleft_frames

    frostright_frames = []
    for i in range(1, 47):
        frostright_img = p.transform.scale(
            p.image.load(f"frostright/frostrightskill ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        frostright_frames.append(frostright_img)
    IMAGES['frostright_frames'] = frostright_frames

    freeze_frames = []
    for i in range(1, 55):
        freeze_img = p.transform.scale(
            p.image.load(f"freeze/boom ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        freeze_frames.append(freeze_img)
    IMAGES['freeze_frames'] = freeze_frames

    # Tải ảnh vụ nổ kết thúc game
    end_boom_frames = []
    end_num_boom_frames = 81
    for i in range(end_num_boom_frames + 1):
        end_boom_img = p.transform.scale(
            p.image.load(f"endgame_boom/frame00{i:02d}.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        end_boom_frames.append(end_boom_img)
    IMAGES['end_boom_frames'] = end_boom_frames

    # Tải ảnh tia điện kết thúc game
    end_lightning_frames = []
    end_num_lightning_frames = 4
    for i in range(1,end_num_lightning_frames + 1):
        end_lightning_img = p.transform.scale(
            p.image.load(f"endgame_lightning/lightning_skill1_frame{i}.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        end_lightning_frames.append(end_lightning_img)
    IMAGES['end_lightning_frames'] = end_lightning_frames

    magic_frames = []
    for i in range(1, 65):
        magic_img = p.transform.scale(
            p.image.load(f"b_magic/magic ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        magic_frames.append(magic_img)
    IMAGES['magic_frames'] = magic_frames

    magic_move_frames = []
    for i in range(1, 61):
        magic_move_img = p.transform.scale(
            p.image.load(f"b_move/move_ ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        magic_move_frames.append(magic_move_img)
    IMAGES['magic_move_frames'] = magic_move_frames

    magic_boom_frames = []
    for i in range(1, 11):
        magic_boom_img = p.transform.scale(
            p.image.load(f"b_boom/boom_ ({i}).png"), (SQ_SIZE * 3, SQ_SIZE * 3)
        )
        magic_boom_frames.append(magic_boom_img)
    IMAGES['magic_boom_frames'] = magic_boom_frames

    transfer_frames=[]
    num_transfer_frames=86
    for i in range(1, num_transfer_frames + 1):
        transfer_img = p.transform.scale(
            p.image.load(f"transfer/transfer ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        transfer_frames.append(transfer_img)
    IMAGES['transfer_frames'] = transfer_frames

    # Phong cấp 
def showPromotionWindow(screen, color):
    choices = ["Q", "R", "B", "N"]
    width, height = 4 * SQ_SIZE, SQ_SIZE

    x = 2 * SQ_SIZE  # Cột 3
    y = 3 * SQ_SIZE

    rects = []

    # Viền đen 
    border_rect = p.Rect(x - 4, y - 4, width + 8, height + 8)
    p.draw.rect(screen, p.Color("black"), border_rect, border_radius=5)

    promotion_bg = p.Surface((width, height))
    promotion_bg.fill(p.Color("darkgray"))  
    screen.blit(promotion_bg, (x, y))

    #đường viền trắng 
    inner_border = p.Rect(x, y, width, height)
    p.draw.rect(screen, p.Color("white"), inner_border, 2)

    # Vẽ các ô vuông 
    for i in range(1, 4):
        p.draw.line(screen, p.Color("black"), (x + i * SQ_SIZE, y), (x + i * SQ_SIZE, y + height), 3)

    # Vẽ các quân cờ 
    for i, ch in enumerate(choices):
        piece_code = color + ch
        img = IMAGES[piece_code]
        pos_x = x + i * SQ_SIZE + (SQ_SIZE - img.get_width()) // 2
        pos_y = y + (SQ_SIZE - img.get_height()) // 2
        screen.blit(img, (pos_x, pos_y))
        rects.append((p.Rect(x + i * SQ_SIZE, y, SQ_SIZE, SQ_SIZE), ch))

    p.display.flip()
    # Đợi người chơi chọn
    while True:
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN:
                mouse_pos = e.pos
                for rect, ch in rects:
                    if rect.collidepoint(mouse_pos):
                        return ch

def drawBoard(screen, sqSelected, validMoves,flip=False):
    """Draw the chessboard with highlights for selected squares and valid moves, and draw coordinates."""
    colors = [p.Color("white"), p.Color("#779556")]
    highlight = p.Color("blue")
    move_img = p.transform.scale(p.image.load("move.png"), (SQ_SIZE, SQ_SIZE))
    
    screen.fill(p.Color("white"))

    font = p.font.SysFont("Arial", 20, True)
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            real_r = r
            real_c = c
            if flip:
                real_r = DIMENSION - 1 - r
                real_c = DIMENSION - 1 - c

            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(MARGIN+c * SQ_SIZE, real_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            # Highlight selected square
            if sqSelected == (r, c):
                p.draw.rect(screen, highlight, p.Rect(MARGIN + real_c * SQ_SIZE, real_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif (r, c) in validMoves:
                screen.blit(move_img, (MARGIN + real_c * SQ_SIZE, real_r * SQ_SIZE))

            # Draw rank on the first column
            if c == 0:
                label = font.render(ranks[r], True, p.Color("black"))
                screen.blit(label, (5, real_r * SQ_SIZE + 25 ))

            # Draw file on the bottom row
            if r == 7:
                label = font.render(files[c], True, p.Color("black"))
                screen.blit(label, (MARGIN + real_c * SQ_SIZE + SQ_SIZE //2 - 5, HEIGHT - 5 ))


def drawPieces(screen, board,flip=False):
    """Draw chess pieces on the board."""
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            real_r = r
            real_c = c
            if flip:
                real_r = DIMENSION - 1 - r
                real_c = DIMENSION - 1 - c
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(MARGIN+ real_c * SQ_SIZE, real_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs, sqSelected, validMoves,flip_board):
    """Draw the entire game state (board + pieces)."""
    drawBoard(screen, sqSelected, validMoves,flip_board)
    drawPieces(screen, gs.board,flip_board)

captured_white = []
captured_black = []

def drawCapturedPieces(screen, captured_white, captured_black):
    background_color = p.Color(222, 184, 135)  # Màu nâu nhạt
    p.draw.rect(screen, background_color, p.Rect(HEIGHT + MARGIN, 0, INFO_WIDTH, HEIGHT + MARGIN))

    piece_size = 30
    spacing = 5

    x_offset_black = WIDTH+MARGIN+20
    y_offset_black = 20
    for i, piece in enumerate(captured_black):
        img = p.transform.scale(IMAGES[piece], (piece_size, piece_size))
        screen.blit(img, (x_offset_black , y_offset_black + i * (piece_size + spacing)))


    x_offset_white = WIDTH+ MARGIN + 100
    y_offset_white = 20
    for i, piece in enumerate(captured_white):
        img = p.transform.scale(IMAGES[piece], (piece_size, piece_size))
        screen.blit(img, (x_offset_white, y_offset_white + i * (piece_size + spacing)))


def main(two_player):
    """Main game loop."""
    p.init()
    move_window = MoveHistoryWindow()
    p.mixer.init()
    flip_board = False

    move_sound1 = p.mixer.Sound("sounds/chessmove1.wav")
    move_sound2 = p.mixer.Sound("sounds/chessmove2.wav")
    move_sound3 = p.mixer.Sound("sounds/chesscapture.wav")
    endgame_explosion_sound = p.mixer.Sound("sounds/hq-explosion-6288.wav")
    endgame_explosion_sound.set_volume(0.3)
    endgame_lightning_sound = p.mixer.Sound("sounds/electric-sparks-6130.wav")

    
    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    loadImages()

    running = True
    sqSelected = ""
    playerClicks = []
    validMoves = []

    while running:    
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = (location[0]-MARGIN) // SQ_SIZE
                row = location[1] // SQ_SIZE
                if flip_board:
                    row = 7 - row
                    col = 7 - col
                if (0<= row <8 and 0 <= col <8): 
                    if sqSelected == (row, col):
                        sqSelected = ""
                        playerClicks = []
                        validMoves = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                        if len(playerClicks) == 1:
                            piece = gs.board[row][col]
                            if (gs.white_to_move and piece.startswith("w")) or \
                            (not gs.white_to_move and piece.startswith("b")):
                                move = ChessEngine.Move(playerClicks[0], playerClicks[0], gs.board)
                                validMoves = gs.wayToMove(move)
                                move_sound1.play()

                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            if gs.checkMove(move):
                                if move.pieceCaptured != "--":
                                    if move.pieceCaptured[0] == 'w':
                                        captured_white.append(move.pieceCaptured)
                                    else:
                                        captured_black.append(move.pieceCaptured)
                                if move.pieceMoved in ["wN", "bN"]:
                                    animateMoveKnight(
                                        move, screen, gs.board, clock,
                                        IMAGES['Slash_color1_frame1'], IMAGES['boom_frames'],
                                        IMAGES, SQ_SIZE, "lightning"
                                    )
                                elif move.pieceMoved in ["wp", "bp"]:
                                    animateMovePawn(
                                        move, screen, gs.board, clock,
                                        IMAGES['p_Slash_color1_frame1'], IMAGES['p_boom_frames'],
                                        IMAGES, SQ_SIZE, "lightning"
                                    )
                                elif move.pieceMoved in ["wR", "bR"]:
                                    animateMoveRook(
                                        move, screen, gs.board, clock,
                                        IMAGES['freeze_frames'], IMAGES['frost_frames'],
                                        IMAGES['frostright_frames'], IMAGES['frostleft_frames'],
                                        IMAGES, SQ_SIZE
                                    )
                                elif move.pieceMoved in ["wB", "bB"]:
                                    animateMoveBishop(
                                        move, screen, gs.board, clock,
                                        IMAGES['magic_frames'], IMAGES['magic_boom_frames'],
                                        IMAGES['magic_move_frames'],
                                        IMAGES, SQ_SIZE
                                    )
                                gs.makeMove(move)
                                if two_player:
                                    flip_board = not flip_board

                                move_window.add_move(move.getFullNotation(), move)

                                if (move.pieceMoved.endswith("p") and ((move.pieceMoved.startswith("w") and move.endRow == 0) or (move.pieceMoved.startswith("b") and move.endRow == 7))):
                                    drawGameState(screen, gs, None, [])
                                    promoted_piece = showPromotionWindow(screen, move.pieceMoved[0])  # Lấy ký tự Q, R, B, N
                                    gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + promoted_piece 
                                    if promoted_piece=='N':
                                        animatetransfer(move,screen,gs.board,clock,IMAGES['transfer_frames'],1,21,IMAGES, SQ_SIZE)
                                    if promoted_piece=='R':
                                        animatetransfer(move,screen,gs.board,clock,IMAGES['transfer_frames'],21,43,IMAGES, SQ_SIZE)
                                    if promoted_piece=='Q':
                                        animatetransfer(move,screen,gs.board,clock,IMAGES['transfer_frames'],43,65,IMAGES, SQ_SIZE)
                                    if promoted_piece=='B':
                                        animatetransfer(move,screen,gs.board,clock,IMAGES['transfer_frames'],65,88,IMAGES, SQ_SIZE)
                                if move.pieceCaptured == "--":
                                    move_sound2.play()
                                else:
                                    move_sound3.play()
                                sqSelected = ""
                                playerClicks = []
                                validMoves = []
                            else:
                                playerClicks = [playerClicks[0]]
                                sqSelected = playerClicks[0]
                                move = ChessEngine.Move(playerClicks[0], playerClicks[0], gs.board)
                                validMoves = gs.wayToMove(move)

        drawGameState(screen, gs, sqSelected, validMoves,flip_board)
        drawCapturedPieces(screen, captured_white, captured_black)

        if gs.checkmate:
            result = animateCheckmate(screen, gs.board, clock, IMAGES['freeze_frames'], IMAGES['end_boom_frames'], gs, endgame_explosion_sound,WIDTH,HEIGHT,IMAGES,SQ_SIZE)
            print("Checkmate! Game over.")
            if result == "replay":
                gs = ChessEngine.GameState()  # Reset game state
                sqSelected = ()
                playerClicks = []
                validMoves = []
            elif result == "back" or result == "quit":
                running = False
        elif gs.stalemate:
            result = animateStalemate(screen, gs.board, clock, IMAGES['end_lightning_frames'], gs, endgame_lightning_sound,WIDTH,HEIGHT,IMAGES,SQ_SIZE)
            print("Stalemate! Game over.")
            if result == "replay":
                gs = ChessEngine.GameState()
                sqSelected = ()
                playerClicks = []
                validMoves = []
            elif result == "back" or result == "quit":
                running = False
        move_window.update()
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()
if __name__ == "__main__":
    main()