import pygame as p
import ChessEngine

# Constants
WIDTH = HEIGHT = 650
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK',
              'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    
    # Tải ảnh quả cầu lửa
    fireball_frames = []
    num_frames = 60
    for i in range(1, num_frames + 1):
        fireball_img = p.transform.scale(
            p.image.load(f"16_sunburn_spritesheet/{i}_16_sunburn_spritesheet.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        fireball_frames.append(fireball_img)
    IMAGES['fireball_frames'] = fireball_frames

    # Tải ảnh vụ nổ
    boom_frames = []
    num_boom_frames = 12
    for i in range(1, num_boom_frames + 1):
        boom_img = p.transform.scale(
            p.image.load(f"03/{39+i}_03.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        boom_frames.append(boom_img)
    IMAGES['boom_frames'] = boom_frames

    Slash_color1_frame1 = []
    num_Slash_color1_frames = 9
    for i in range(1, num_Slash_color1_frames + 1):
        Slash_color1_img = p.transform.scale(
            p.image.load(f"Frames/Slash_color1_frame{i}.png"), (SQ_SIZE * 3, SQ_SIZE * 3)
        )
        Slash_color1_frame1.append(Slash_color1_img)
    IMAGES['Slash_color1_frame1'] = Slash_color1_frame1

    # Con tốt
    # Tải ảnh vụ nổ
    p_boom_frames = []
    p_num_boom_frames = 12
    for i in range(256, 256 + p_num_boom_frames + 1):
        p_boom_img = p.transform.scale(
            p.image.load(f"p_smoke/{i}_Smoke.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        p_boom_frames.append(p_boom_img)
    IMAGES['p_boom_frames'] = p_boom_frames

    p_Slash_color1_frame1 = []
    p_num_Slash_color1_frames = 10
    for i in range(1, p_num_Slash_color1_frames + 1):
        p_Slash_color1_img = p.transform.scale(
            p.image.load(f"p_Frames/warrior_skill1_frame{i}.png"), (SQ_SIZE * 3, SQ_SIZE * 3)
        )
        p_Slash_color1_frame1.append(p_Slash_color1_img)
    IMAGES['p_Slash_color1_frame1'] = p_Slash_color1_frame1


    #load image
    frost_frames=[]
    num_frames=57
    for i in range(1, num_frames + 1):
        frost_img = p.transform.scale(
            p.image.load(f"frost/frost ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        frost_frames.append(frost_img)
    IMAGES['frost_frames'] = frost_frames

    frostleft_frames=[]
    num_frames=46
    for i in range(1, num_frames + 1):
        frostleft_img = p.transform.scale(
            p.image.load(f"frostleft/frostleft ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        frostleft_frames.append(frostleft_img)
    IMAGES['frostleft_frames'] = frostleft_frames

    frostright_frames=[]
    num_frames=46
    for i in range(1, num_frames + 1):
        frostright_img = p.transform.scale(
            p.image.load(f"frostright/frostrightskill ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        frostright_frames.append(frostright_img)
    IMAGES['frostright_frames'] = frostright_frames

    freeze_frames=[]
    num_freeze_frames=54
    for i in range(1, num_freeze_frames + 1):
        freeze_img = p.transform.scale(
            p.image.load(f"freeze/boom ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        freeze_frames.append(freeze_img)
    IMAGES['freeze_frames'] = freeze_frames



def drawBoard(screen, sqSelected, validMoves):
    colors = [p.Color("white"), p.Color("#779556")]
    HIGHLIGHT = p.Color("blue")
    move_img = p.image.load("move.png") 
    move_img = p.transform.scale(move_img, (SQ_SIZE, SQ_SIZE))
     

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if sqSelected == (r, c):
                p.draw.rect(screen, HIGHLIGHT, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif (r, c) in validMoves:
                screen.blit(move_img, (c * SQ_SIZE, r * SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawGameState(screen, gs, sqSelected, validMoves):
    drawBoard(screen, sqSelected, validMoves)
    drawPieces(screen, gs.board)

def animateMoveWithEffect(move, screen, board, clock, effect_frames, boom_frames, effect_type="effect"):
    """
    Hàm chung để tạo animation cho nhiều loại hiệu ứng khác nhau
    :param move: nước đi
    :param screen: màn hình Pygame
    :param board: bàn cờ
    :param clock: đồng hồ Pygame
    :param effect_frames: danh sách các frame của hiệu ứng (fireball, lightning, v.v.)
    :param boom_frames: danh sách các frame của vụ nổ
    :param effect_type: tên của hiệu ứng (dùng để debug hoặc tùy chỉnh nếu cần)
    """
    colors = [p.Color("white"), p.Color("#779556")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 200
    effect_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    boom_frame_count = 200  # Số khung hình cho vụ nổ
    num_effect_frames = len(effect_frames)
    num_boom_frames = len(boom_frames)

    temp_board = [row[:] for row in board]

    if move.pieceCaptured != "--":
        # 1. Hiệu ứng di chuyển (fireball/lightning/...) đến quân địch
        for frame in range(effect_frame_count + 1):
            r = move.startRow + dR * frame / effect_frame_count
            c = move.startCol + dC * frame / effect_frame_count

            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            effect_idx = (frame // 5) % num_effect_frames
            effect_image = effect_frames[effect_idx]
            effect_x = c * SQ_SIZE + (SQ_SIZE - effect_image.get_width()) // 2
            effect_y = r * SQ_SIZE + (SQ_SIZE - effect_image.get_height()) // 2
            screen.blit(effect_image, (effect_x, effect_y))
            
            p.display.flip()
            clock.tick(60)

        # 2. Hiệu ứng vụ nổ tại ô đích
        temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch trước khi vẽ vụ nổ
        temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)

# Cách sử dụng:
# Với fireball
# animateMoveWithEffect(move, screen, board, clock, fireball_frames, boom_frames, "fireball")

# Với lightning
# animateMoveWithEffect(move, screen, board, clock, lightning_frames, boom_frames, "lightning")

def animateMove(move, screen, board, clock):
    temp_board = [row[:] for row in board]
    temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch trước khi vẽ vụ nổ
    temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 20
    move_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    # 3. Di chuyển quân mình từ từ đến ô đích
    for frame in range(move_frame_count + 1):
        r = move.startRow + dR * frame / move_frame_count
        c = move.startCol + dC * frame / move_frame_count

        drawBoard(screen, (), [])
        drawPieces(screen, temp_board)

        piece_x = c * SQ_SIZE
        piece_y = r * SQ_SIZE
        screen.blit(IMAGES[move.pieceMoved], (piece_x, piece_y))
        
        p.display.flip()
        clock.tick(60)

def animateMoveKnight(move, screen, board, clock, effect_frames, boom_frames, effect_type="effect"):
    """
    Hàm chung để tạo animation cho nhiều loại hiệu ứng khác nhau
    :param move: nước đi
    :param screen: màn hình Pygame
    :param board: bàn cờ
    :param clock: đồng hồ Pygame
    :param effect_frames: danh sách các frame của hiệu ứng (fireball, lightning, v.v.)
    :param boom_frames: danh sách các frame của vụ nổ
    :param effect_type: tên của hiệu ứng (dùng để debug hoặc tùy chỉnh nếu cần)
    """
    colors = [p.Color("white"), p.Color("#779556")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 20
    effect_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    boom_frame_count = 20  # Số khung hình cho vụ nổ
    num_effect_frames = len(effect_frames)
    num_boom_frames = len(boom_frames)

    temp_board = [row[:] for row in board]
    temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ
    if move.pieceCaptured != "--":
        # hiệu ứng nổ ở ô bắt đầu 
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)
        # hiệu ứng chém ở ô đích
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_effect_frames // boom_frame_count) % num_effect_frames
            boom_image = effect_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)


        temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch sau khi bị chém 

        #  Hiệu ứng vụ nổ tại ô đích 
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)
        # 2. Hiệu ứng vụ nổ tại ô đầu tiên
        temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch trước khi vẽ vụ nổ
        temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ
        screen.blit(IMAGES[move.pieceMoved], (move.endRow, move.endCol))
    else:
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch trước khi vẽ vụ nổ
        temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)

def animateMovePawn(move, screen, board, clock, effect_frames, boom_frames, effect_type="effect"):
    """
    Hàm chung để tạo animation cho nhiều loại hiệu ứng khác nhau
    :param move: nước đi
    :param screen: màn hình Pygame
    :param board: bàn cờ
    :param clock: đồng hồ Pygame
    :param effect_frames: danh sách các frame của hiệu ứng (fireball, lightning, v.v.)
    :param boom_frames: danh sách các frame của vụ nổ
    :param effect_type: tên của hiệu ứng (dùng để debug hoặc tùy chỉnh nếu cần)
    """
    colors = [p.Color("white"), p.Color("#779556")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 15
    effect_frame_count = int((abs(dR) + abs(dC)) * frames_per_square)
    boom_frame_count = 20  # Số khung hình cho vụ nổ
    num_effect_frames = len(effect_frames)
    num_boom_frames = len(boom_frames)

    temp_board = [row[:] for row in board]
    temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ
    if move.pieceCaptured != "--":
        # hiệu ứng nổ ở ô bắt đầu 
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)
        # hiệu ứng chém ở ô đích
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_effect_frames // boom_frame_count) % num_effect_frames
            boom_image = effect_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)


        temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch sau khi bị chém 

        #  Hiệu ứng vụ nổ tại ô đích 
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)
        # 2. Hiệu ứng vụ nổ tại ô đầu tiên
        temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch trước khi vẽ vụ nổ
        temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ
        screen.blit(IMAGES[move.pieceMoved], (move.endRow, move.endCol))
    else:
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"  # Xóa quân địch trước khi vẽ vụ nổ
        temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            
            p.display.flip()
            clock.tick(60)

def animateMoveRook(move, screen, board, clock, freeze_frames, frost_frames,frostright_frames,frostleft_frames):
    colors = [p.Color("white"), p.Color("#779556")]
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 20
    frost_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    frostright_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    frostleft_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    freeze_frame_count = 20  
    move_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    num_frost_frames = len(frost_frames)
    num_freeze_frames = len(freeze_frames)
    num_frostright_frames =len(frostright_frames)
    num_frostleft_frames =len(frostright_frames)

    temp_board = [row[:] for row in board]

    if move.pieceCaptured != "--":
        if move.startCol == move.endCol:
           
            for frame in range(6):
                drawBoard(screen, (), [])
                drawPieces(screen, temp_board)

                frost_idx = frame % num_frost_frames
                frost_image = frost_frames[frost_idx]
                frost_x = move.startCol * SQ_SIZE + (SQ_SIZE - frost_image.get_width()) // 2
                frost_y = move.startRow * SQ_SIZE + (SQ_SIZE - frost_image.get_height()) // 2
                screen.blit(frost_image, (frost_x, frost_y))

                p.display.flip()
                clock.tick(10)         
            for frame in range(6,11):
                drawBoard(screen, (), [])
                drawPieces(screen, temp_board)

                frost_idx = frame % num_frost_frames
                frost_image = frost_frames[frost_idx]
                frost_x = move.endCol * SQ_SIZE + (SQ_SIZE - frost_image.get_width()) // 2
                frost_y = move.endRow * SQ_SIZE + (SQ_SIZE - frost_image.get_height()) // 2
                screen.blit(frost_image, (frost_x, frost_y))

                p.display.flip()
                clock.tick(10)
            for frame in range(11,58):
                drawBoard(screen, (), [])
                drawPieces(screen, temp_board)

                frost_idx = frame % num_frost_frames
                frost_image = frost_frames[frost_idx]
                frost_x = move.endCol * SQ_SIZE + (SQ_SIZE - frost_image.get_width()) // 2
                frost_y = move.endRow * SQ_SIZE + (SQ_SIZE - frost_image.get_height()) // 1.5
                screen.blit(frost_image, (frost_x, frost_y))
                p.display.flip()
                clock.tick(30)
        if move.startCol < move.endCol:
            for frame in range(frostright_frame_count + 1):
                r = move.startRow + dR * frame / frostright_frame_count
                c = move.startCol + dC * frame / frostright_frame_count

                drawBoard(screen, (), [])
                drawPieces(screen, temp_board)

                frostright_idx = (frame // 5) % num_frostright_frames
                frostright_image = frostright_frames[frostright_idx]
                scale_factor = 2.0 
                frostright_image = p.transform.scale(frostright_frames[frostright_idx], 
                                     (int(frostright_frames[frostright_idx].get_width() * scale_factor), 
                                      int(frostright_frames[frostright_idx].get_height() * scale_factor)))
                frostright_x = c * SQ_SIZE + (SQ_SIZE - frostright_image.get_width()) // 2
                frostright_y = r * SQ_SIZE + (SQ_SIZE - frostright_image.get_height()) // 1.8
                screen.blit(frostright_image, (frostright_x, frostright_y))
                
                p.display.flip()
                clock.tick(60)
        if move.startCol > move.endCol:
            for frame in range(frostleft_frame_count + 1):
                r = move.startRow + dR * frame / frostleft_frame_count
                c = move.startCol + dC * frame / frostleft_frame_count

                drawBoard(screen, (), [])
                drawPieces(screen, temp_board)

                frostleft_idx = (frame // 5) % num_frostleft_frames
                frostleft_image = frostleft_frames[frostleft_idx]
                scale_factor = 2.0 
                frostleft_image = p.transform.scale(frostleft_frames[frostleft_idx], 
                                     (int(frostleft_frames[frostleft_idx].get_width() * scale_factor), 
                                      int(frostleft_frames[frostleft_idx].get_height() * scale_factor)))
                frostleft_x = c * SQ_SIZE + (SQ_SIZE - frostleft_image.get_width()) // 2
                frostleft_y = r * SQ_SIZE + (SQ_SIZE - frostleft_image.get_height()) // 1.8
                screen.blit(frostleft_image, (frostleft_x, frostleft_y))
                
                p.display.flip()
                clock.tick(60)

        
        for frame in range(freeze_frame_count + 1):
            drawBoard(screen, (), [])
            drawPieces(screen, temp_board)

            freeze_idx = (frame * num_freeze_frames // freeze_frame_count) % num_freeze_frames  
            freeze_image = freeze_frames[freeze_idx]
            scale_factor = 2
            freeze_image = p.transform.scale(freeze_frames[freeze_idx], 
                                     (int(freeze_frames[freeze_idx].get_width() * scale_factor), 
                                      int(freeze_frames[freeze_idx].get_height() * scale_factor)))
            freeze_x = move.endCol * SQ_SIZE + (SQ_SIZE - freeze_image.get_width()) // 2.0
            freeze_y = move.endRow * SQ_SIZE + (SQ_SIZE - freeze_image.get_height()) // 1.8
            screen.blit(freeze_image, (freeze_x, freeze_y))
            
            p.display.flip()
            clock.tick(40)
    temp_board[move.endRow][move.endCol] = "--"  
    temp_board[move.startRow][move.startCol] = "--"  # Xóa quân mình trước khi vẽ vụ nổ
    # 3. Di chuyển quân mình từ từ đến ô đích
    
    for frame in range(move_frame_count + 1):
        r = move.startRow + dR * frame / move_frame_count
        c = move.startCol + dC * frame / move_frame_count

        drawBoard(screen, (), [])
        drawPieces(screen, temp_board)

        piece_x = c * SQ_SIZE
        piece_y = r * SQ_SIZE
        screen.blit(IMAGES[move.pieceMoved], (piece_x, piece_y))
        
        p.display.flip()
        clock.tick(90)
    #frost_sound2.stop()

 
        

 


def main():
    p.init()
    p.mixer.init()

    move_sound1 = p.mixer.Sound("sounds/chessmove1.wav")
    move_sound2 = p.mixer.Sound("sounds/chessmove2.wav")
    move_sound3 = p.mixer.Sound("sounds/chesscapture.wav")

    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()

    running = True
    sqSelected = ()
    playerClicks = []
    validMoves = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                    validMoves = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)

                    if len(playerClicks) == 1:
                        piece = gs.board[row][col]
                        if (gs.white_to_move and piece.startswith("w")) or (not gs.white_to_move and piece.startswith("b")):
                            move = ChessEngine.Move(playerClicks[0], playerClicks[0], gs.board)
                            validMoves = gs.wayToMove(move)
                            move_sound1.play()

                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        if gs.checkMove(move):
                            if move.pieceMoved == "wN" or move.pieceMoved == "bN":
                                animateMoveKnight(move, screen, gs.board, clock, IMAGES['Slash_color1_frame1'], IMAGES['boom_frames'], "lightning")
                            if move.pieceMoved == "wp" or move.pieceMoved == "bp":
                                animateMovePawn(move, screen, gs.board, clock, IMAGES['p_Slash_color1_frame1'], IMAGES['p_boom_frames'], "lightning")
                            if move.pieceMoved == "wR" or move.pieceMoved == "bR":
                                animateMoveRook(move, screen, gs.board, clock, IMAGES['freeze_frames'], IMAGES['frost_frames'], IMAGES['frostright_frames'], IMAGES['frostleft_frames'])\

                            # animateMove(move, screen, gs.board, clock)
                            gs.makeMove(move)
                            if move.pieceCaptured == "--":
                                move_sound2.play()
                            else:
                                move_sound3.play()
                            sqSelected = ()
                            playerClicks = []
                            validMoves = []
                        else:
                            playerClicks = [playerClicks[0]]
                            sqSelected = playerClicks[0]
                            move = ChessEngine.Move(playerClicks[0], playerClicks[0], gs.board)
                            validMoves = gs.wayToMove(move)

        drawGameState(screen, gs, sqSelected, validMoves)

        if gs.checkmate:
            print("Checkmate! Game over.")
            running = False
        elif gs.stalemate:
            print("Stalemate! Game over.")
            running = False

        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()