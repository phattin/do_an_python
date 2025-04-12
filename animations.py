import pygame as p

def animateMoveWithEffect(move, screen, board, clock, effect_frames, boom_frames, IMAGES, SQ_SIZE, effect_type="effect"):
    """
    Animate a move with an effect (e.g., fireball) and explosion for captures.
    """
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 200
    effect_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    boom_frame_count = 200
    num_effect_frames = len(effect_frames)
    num_boom_frames = len(boom_frames)

    temp_board = [row[:] for row in board]

    if move.pieceCaptured != "--":
        for frame in range(effect_frame_count + 1):
            r = move.startRow + dR * frame / effect_frame_count
            c = move.startCol + dC * frame / effect_frame_count
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            effect_idx = (frame // 5) % num_effect_frames
            effect_image = effect_frames[effect_idx]
            effect_x = c * SQ_SIZE + (SQ_SIZE - effect_image.get_width()) // 2
            effect_y = r * SQ_SIZE + (SQ_SIZE - effect_image.get_height()) // 2
            screen.blit(effect_image, (effect_x, effect_y))
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"
        temp_board[move.startRow][move.startCol] = "--"
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

def animateMove(move, screen, board, clock, IMAGES, SQ_SIZE):
    """Animate a piece moving smoothly to its destination."""
    temp_board = [row[:] for row in board]
    temp_board[move.endRow][move.endCol] = "--"
    temp_board[move.startRow][move.startCol] = "--"
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 20
    move_frame_count = (abs(dR) + abs(dC)) * frames_per_square

    for frame in range(move_frame_count + 1):
        r = move.startRow + dR * frame / move_frame_count
        c = move.startCol + dC * frame / move_frame_count
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        piece_x = c * SQ_SIZE
        piece_y = r * SQ_SIZE
        screen.blit(IMAGES[move.pieceMoved], (piece_x, piece_y))
        p.display.flip()
        clock.tick(60)

def animateMoveKnight(move, screen, board, clock, effect_frames, boom_frames, IMAGES, SQ_SIZE, effect_type="effect"):
    """Animate knight moves with slash and explosion effects."""
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 20
    effect_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    boom_frame_count = 20
    num_effect_frames = len(effect_frames)
    num_boom_frames = len(boom_frames)

    temp_board = [row[:] for row in board]
    temp_board[move.startRow][move.startCol] = "--"

    if move.pieceCaptured != "--":
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_effect_frames // boom_frame_count) % num_effect_frames
            boom_image = effect_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)
    else:
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"
        temp_board[move.startRow][move.startCol] = "--"

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

def animateMovePawn(move, screen, board, clock, effect_frames, boom_frames, IMAGES, SQ_SIZE, effect_type="effect"):
    """Animate pawn moves with slash and explosion effects."""
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 15
    effect_frame_count = int((abs(dR) + abs(dC)) * frames_per_square)
    boom_frame_count = 20
    num_effect_frames = len(effect_frames)
    num_boom_frames = len(boom_frames)

    temp_board = [row[:] for row in board]
    temp_board[move.startRow][move.startCol] = "--"

    if move.pieceCaptured != "--":
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_effect_frames // boom_frame_count) % num_effect_frames
            boom_image = effect_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)
    else:
        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.startCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.startRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"
        temp_board[move.startRow][move.startCol] = "--"

        for frame in range(boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_boom_frames // boom_frame_count) % num_boom_frames
            boom_image = boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

def animateMoveRook(move, screen, board, clock, freeze_frames, frost_frames, frostright_frames, frostleft_frames, IMAGES, SQ_SIZE):
    """Animate rook moves with frost and freeze effects."""
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 20
    frost_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    freeze_frame_count = 20
    move_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    num_frost_frames = len(frost_frames)
    num_freeze_frames = len(freeze_frames)
    num_frostright_frames = len(frostright_frames)
    num_frostleft_frames = len(frostleft_frames)

    temp_board = [row[:] for row in board]

    if move.pieceCaptured != "--":
        if move.startCol == move.endCol:
            for frame in range(6):
                drawBoard(screen, (), [], SQ_SIZE)
                drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
                frost_idx = frame % num_frost_frames
                frost_image = frost_frames[frost_idx]
                frost_x = move.startCol * SQ_SIZE + (SQ_SIZE - frost_image.get_width()) // 2
                frost_y = move.startRow * SQ_SIZE + (SQ_SIZE - frost_image.get_height()) // 2
                screen.blit(frost_image, (frost_x, frost_y))
                p.display.flip()
                clock.tick(10)

            for frame in range(6, 11):
                drawBoard(screen, (), [], SQ_SIZE)
                drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
                frost_idx = frame % num_frost_frames
                frost_image = frost_frames[frost_idx]
                frost_x = move.endCol * SQ_SIZE + (SQ_SIZE - frost_image.get_width()) // 2
                frost_y = move.endRow * SQ_SIZE + (SQ_SIZE - frost_image.get_height()) // 2
                screen.blit(frost_image, (frost_x, frost_y))
                p.display.flip()
                clock.tick(10)

            for frame in range(11, 58):
                drawBoard(screen, (), [], SQ_SIZE)
                drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
                frost_idx = frame % num_frost_frames
                frost_image = frost_frames[frost_idx]
                frost_x = move.endCol * SQ_SIZE + (SQ_SIZE - frost_image.get_width()) // 2
                frost_y = move.endRow * SQ_SIZE + (SQ_SIZE - frost_image.get_height()) // 1.5
                screen.blit(frost_image, (frost_x, frost_y))
                p.display.flip()
                clock.tick(30)

        elif move.startCol < move.endCol:
            for frame in range(frost_frame_count + 1):
                r = move.startRow + dR * frame / frost_frame_count
                c = move.startCol + dC * frame / frost_frame_count
                drawBoard(screen, (), [], SQ_SIZE)
                drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
                frostright_idx = (frame // 5) % num_frostright_frames
                frostright_image = p.transform.scale(
                    frostright_frames[frostright_idx],
                    (int(frostright_frames[frostright_idx].get_width() * 2.0),
                     int(frostright_frames[frostright_idx].get_height() * 2.0))
                )
                frostright_x = c * SQ_SIZE + (SQ_SIZE - frostright_image.get_width()) // 2
                frostright_y = r * SQ_SIZE + (SQ_SIZE - frostright_image.get_height()) // 1.8
                screen.blit(frostright_image, (frostright_x, frostright_y))
                p.display.flip()
                clock.tick(60)

        elif move.startCol > move.endCol:
            for frame in range(frost_frame_count + 1):
                r = move.startRow + dR * frame / frost_frame_count
                c = move.startCol + dC * frame / frost_frame_count
                drawBoard(screen, (), [], SQ_SIZE)
                drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
                frostleft_idx = (frame // 5) % num_frostleft_frames
                frostleft_image = p.transform.scale(
                    frostleft_frames[frostleft_idx],
                    (int(frostleft_frames[frostleft_idx].get_width() * 2.0),
                     int(frostleft_frames[frostleft_idx].get_height() * 2.0))
                )
                frostleft_x = c * SQ_SIZE + (SQ_SIZE - frostleft_image.get_width()) // 2
                frostleft_y = r * SQ_SIZE + (SQ_SIZE - frostleft_image.get_height()) // 1.8
                screen.blit(frostleft_image, (frostleft_x, frostleft_y))
                p.display.flip()
                clock.tick(60)

        for frame in range(freeze_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            freeze_idx = (frame * num_freeze_frames // freeze_frame_count) % num_freeze_frames
            freeze_image = p.transform.scale(
                freeze_frames[freeze_idx],
                (int(freeze_frames[freeze_idx].get_width() * 2),
                 int(freeze_frames[freeze_idx].get_height() * 2))
            )
            freeze_x = move.endCol * SQ_SIZE + (SQ_SIZE - freeze_image.get_width()) // 2.0
            freeze_y = move.endRow * SQ_SIZE + (SQ_SIZE - freeze_image.get_height()) // 1.8
            screen.blit(freeze_image, (freeze_x, freeze_y))
            p.display.flip()
            clock.tick(40)

    temp_board[move.endRow][move.endCol] = "--"
    temp_board[move.startRow][move.startCol] = "--"

    for frame in range(move_frame_count + 1):
        r = move.startRow + dR * frame / move_frame_count
        c = move.startCol + dC * frame / move_frame_count
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        piece_x = c * SQ_SIZE
        piece_y = r * SQ_SIZE
        screen.blit(IMAGES[move.pieceMoved], (piece_x, piece_y))
        p.display.flip()
        clock.tick(90)

def animateMoveBishop(move, screen, board, clock, magic_frames, magic_boom_frames, magic_move_frames, IMAGES, SQ_SIZE):
    """Animate bishop moves with magic and explosion effects."""
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    frames_per_square = 20
    magic_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    magic_boom_frame_count = 20
    move_frame_count = (abs(dR) + abs(dC)) * frames_per_square
    num_magic_frames = len(magic_frames)
    num_magic_boom_frames = len(magic_boom_frames)

    temp_board = [row[:] for row in board]

    if move.pieceCaptured != "--":
        for frame in range(magic_frame_count + 1):
            r = move.startRow + dR * frame / magic_frame_count
            c = move.startCol + dC * frame / magic_frame_count
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            magic_idx = (frame // 5) % num_magic_frames
            magic_image = magic_frames[magic_idx]
            magic_x = c * SQ_SIZE + (SQ_SIZE - magic_image.get_width()) // 2
            magic_y = r * SQ_SIZE + (SQ_SIZE - magic_image.get_height()) // 2
            screen.blit(magic_image, (magic_x, magic_y))
            p.display.flip()
            clock.tick(60)

        temp_board[move.endRow][move.endCol] = "--"
        for frame in range(magic_boom_frame_count + 1):
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            boom_idx = (frame * num_magic_boom_frames // magic_boom_frame_count) % num_magic_boom_frames
            boom_image = magic_boom_frames[boom_idx]
            boom_x = move.endCol * SQ_SIZE + (SQ_SIZE - boom_image.get_width()) // 2
            boom_y = move.endRow * SQ_SIZE + (SQ_SIZE - boom_image.get_height()) // 2
            screen.blit(boom_image, (boom_x, boom_y))
            p.display.flip()
            clock.tick(60)

    temp_board[move.startRow][move.startCol] = "--"
    trail_effects = []

    for frame in range(move_frame_count + 1):
        r = move.startRow + dR * frame / move_frame_count
        c = move.startCol + dC * frame / move_frame_count
        if frame % 3 == 0:
            trail_effects.append((r, c, 255))
        for i in range(len(trail_effects)):
            tr, tc, alpha = trail_effects[i]
            trail_effects[i] = (tr, tc, max(0, alpha - 5))
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        for tr, tc, alpha in trail_effects:
            trail_img = magic_move_frames[(frame // 5) % len(magic_move_frames)]
            trail_img.set_alpha(alpha)
            trail_x = tc * SQ_SIZE + (SQ_SIZE - trail_img.get_width()) // 2
            trail_y = tr * SQ_SIZE + (SQ_SIZE - trail_img.get_height()) // 2
            screen.blit(trail_img, (trail_x, trail_y))
        piece_x = c * SQ_SIZE
        piece_y = r * SQ_SIZE
        screen.blit(IMAGES[move.pieceMoved], (piece_x, piece_y))
        p.display.flip()
        clock.tick(120)

def drawBoard(screen, sqSelected, validMoves, SQ_SIZE):
    """Draw the chessboard with highlights for selected squares and valid moves."""
    colors = [p.Color("white"), p.Color("#779556")]
    highlight = p.Color("blue")
    move_img = p.transform.scale(p.image.load("move.png"), (SQ_SIZE, SQ_SIZE))

    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            if sqSelected == (r, c):
                p.draw.rect(screen, highlight, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif (r, c) in validMoves:
                screen.blit(move_img, (c * SQ_SIZE, r * SQ_SIZE))

def drawPieces(screen, board, IMAGES, SQ_SIZE):
    """Draw chess pieces on the board."""
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animatetransfer(move, screen, board, clock,transfer_frames,n,m,IMAGES,SQ_SIZE):
    transfer_frame_count = 90  # Số khung hình cho vụ nổ
    num_transfer_frames = len(transfer_frames)

    temp_board = [row[:] for row in board]
    for frame in range(n,m):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)

        transfer_idx = (frame * num_transfer_frames // transfer_frame_count) % num_transfer_frames  # Chọn ảnh vụ nổ
        transfer_image = transfer_frames[transfer_idx]
        scale_factor = 0.6
        transfer_image = p.transform.scale(transfer_frames[transfer_idx], 
                            (int(transfer_frames[transfer_idx].get_width() * scale_factor), 
                            int(transfer_frames[transfer_idx].get_height() * scale_factor)))
        transfer_x = move.endCol * SQ_SIZE + (SQ_SIZE - transfer_image.get_width()) // 2
        transfer_y = move.endRow * SQ_SIZE + (SQ_SIZE - transfer_image.get_height()) // 2
        screen.blit(transfer_image, (transfer_x, transfer_y))
        p.display.flip()
        clock.tick(20)
        # hiệu ứng kết thúc game
def animateCheckmate(screen, board, clock, freeze_frames, boom_frames, gs, explosion_sound,WIDTH,HEIGHT,IMAGES,SQ_SIZE):
    """Hiệu ứng kết thúc game khi bị chiếu hết"""
    loser_color = "w" if gs.white_to_move else "b"
    winner_color = "b" if loser_color == "w" else "w"
    winner_name = "Đen" if winner_color == "b" else "Trắng"
    loser_king_pos = gs.white_king_location if loser_color == "w" else gs.black_king_location
    winner_king_pos = gs.black_king_location if winner_color == "b" else gs.white_king_location
    loser_king_piece = "wK" if loser_color == "w" else "bK"
    winner_king_piece = "bK" if winner_color == "b" else "wK"

    num_boom_frames = len(boom_frames)
    king_transition_duration = 30  # Thời gian di chuyển và phóng to
    boom_duration = 30            # Thời gian hiệu ứng nổ
    winner_move_duration = 30     # Thời gian quân vua thắng di chuyển lên trên
    fade_duration = 30

    # Font cho văn bản
    font = p.font.SysFont("Arial", 48, True)
    win_text = font.render(f"{winner_name} Thắng!", True, p.Color("yellow"))
    win_text_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    button_font = p.font.SysFont("Arial", 36, True)
    replay_text = button_font.render("Chơi lại", True, p.Color("white"))
    back_text = button_font.render("Quay lại", True, p.Color("white"))
    replay_rect = replay_text.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2 + 50))
    back_rect = back_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 + 50))

    # Tạo bàn cờ tạm thời và xóa quân vua thua
    temp_board = [row[:] for row in board]
    temp_board[loser_king_pos[0]][loser_king_pos[1]] = "--"

    # 1. Quân vua thua phóng to và di chuyển ra giữa
    loser_start_x = loser_king_pos[1] * SQ_SIZE + SQ_SIZE // 2
    loser_start_y = loser_king_pos[0] * SQ_SIZE + SQ_SIZE // 2
    loser_target_x = WIDTH // 2
    loser_target_y = HEIGHT // 2
    loser_dx = (loser_target_x - loser_start_x) / king_transition_duration
    loser_dy = (loser_target_y - loser_start_y) / king_transition_duration

    for frame in range(king_transition_duration):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        scale_factor = 1 + frame * 2 / king_transition_duration
        king_img = p.transform.scale(IMAGES[loser_king_piece], 
                                    (int(SQ_SIZE * scale_factor), int(SQ_SIZE * scale_factor)))
        king_x = loser_start_x + loser_dx * frame - king_img.get_width() // 2
        king_y = loser_start_y + loser_dy * frame - king_img.get_height() // 2
        screen.blit(king_img, (king_x, king_y))
        p.display.flip()
        clock.tick(60)

    # 2. Hiệu ứng nổ cho quân vua thua
    explosion_sound.set_volume(0.3)
    explosion_sound.play()
    for frame in range(boom_duration):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        boom_idx = (frame * num_boom_frames // boom_duration) % num_boom_frames
        boom_image = p.transform.scale(boom_frames[boom_idx], (SQ_SIZE * 3, SQ_SIZE * 3))
        boom_x = WIDTH // 2 - boom_image.get_width() // 2
        boom_y = HEIGHT // 2 - boom_image.get_height() // 2
        screen.blit(boom_image, (boom_x, boom_y))
        p.display.flip()
        clock.tick(60)

    # 3. Quân vua thắng phóng to và di chuyển lên giữa trên
    winner_start_x = winner_king_pos[1] * SQ_SIZE + SQ_SIZE // 2
    winner_start_y = winner_king_pos[0] * SQ_SIZE + SQ_SIZE // 2
    winner_target_x = WIDTH // 2
    winner_target_y = HEIGHT // 4  # Giữa trên
    winner_dx = (winner_target_x - winner_start_x) / winner_move_duration
    winner_dy = (winner_target_y - winner_start_y) / winner_move_duration

    for frame in range(winner_move_duration):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        scale_factor = 1 + frame * 1 / winner_move_duration  # Phóng to lên 2x
        winner_king_img = p.transform.scale(IMAGES[winner_king_piece], 
                                           (int(SQ_SIZE * scale_factor), int(SQ_SIZE * scale_factor)))
        winner_king_x = winner_start_x + winner_dx * frame - winner_king_img.get_width() // 2
        winner_king_y = winner_start_y + winner_dy * frame - winner_king_img.get_height() // 2
        screen.blit(winner_king_img, (winner_king_x, winner_king_y))
        p.display.flip()
        clock.tick(60)

        # 4. Vòng lặp chờ với quân vua thắng, văn bản và nút
        while True:
            for e in p.event.get():
                if e.type == p.QUIT:
                    return "quit"
                elif e.type == p.MOUSEBUTTONDOWN:
                    pos = p.mouse.get_pos()
                    if replay_rect.collidepoint(pos):
                        return "replay"
                    elif back_rect.collidepoint(pos):
                        return "back"
            
            drawBoard(screen, (), [], SQ_SIZE)
            drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
            
            # Lớp mờ cho toàn màn hình
            overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
            overlay.fill((50, 50, 50, 100))
            screen.blit(overlay, (0, 0))
            
            # Vẽ văn bản và nút
            screen.blit(win_text, win_text_rect)
            p.draw.rect(screen, p.Color("gray"), replay_rect.inflate(20, 10))
            p.draw.rect(screen, p.Color("gray"), back_rect.inflate(20, 10))
            screen.blit(replay_text, replay_rect)
            screen.blit(back_text, back_rect)
            
            # Vẽ quân vua thắng sau overlay để không bị mờ
            winner_king_img = p.transform.scale(IMAGES[winner_king_piece], (int(SQ_SIZE * 2), int(SQ_SIZE * 2)))
            winner_king_x = winner_target_x - winner_king_img.get_width() // 2
            winner_king_y = winner_target_y - winner_king_img.get_height() // 2
            screen.blit(winner_king_img, (winner_king_x, winner_king_y))
            
            p.display.flip()
            clock.tick(60)

    # 2. Hiệu ứng nổ tại vị trí giữa màn hình với âm thanh
    explosion_sound.play()  # Phát âm thanh vụ nổ
    for frame in range(boom_duration):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        
        boom_idx = (frame * num_boom_frames // boom_duration) % num_boom_frames
        boom_image = p.transform.scale(boom_frames[boom_idx], (SQ_SIZE * 3, SQ_SIZE * 3))
        boom_x = WIDTH // 2 - boom_image.get_width() // 2
        boom_y = HEIGHT // 2 - boom_image.get_height() // 2
        screen.blit(boom_image, (boom_x, boom_y))
        
        p.display.flip()
        clock.tick(60)

    # 3. Làm mờ màn hình (không che xám hoàn toàn) và hiển thị văn bản + nút
    for frame in range(fade_duration):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        
        alpha = int(100 * frame / fade_duration)  # Tăng từ 0 đến 100 (mờ nhẹ)
        overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
        overlay.fill((50, 50, 50, alpha))
        screen.blit(overlay, (0, 0))

        screen.blit(win_text, win_text_rect)

        p.draw.rect(screen, p.Color("gray"), replay_rect.inflate(20, 10))
        p.draw.rect(screen, p.Color("gray"), back_rect.inflate(20, 10))
        screen.blit(replay_text, replay_rect)
        screen.blit(back_text, back_rect)
        
        p.display.flip()
        clock.tick(60)

    # 4. Vòng lặp chờ người dùng chọn nút
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                return "quit"
            elif e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if replay_rect.collidepoint(pos):
                    return "replay"
                elif back_rect.collidepoint(pos):
                    return "back"
        
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
        overlay.fill((50, 50, 50, 100))
        screen.blit(overlay, (0, 0))
        screen.blit(win_text, win_text_rect)
        p.draw.rect(screen, p.Color("gray"), replay_rect.inflate(20, 10))
        p.draw.rect(screen, p.Color("gray"), back_rect.inflate(20, 10))
        screen.blit(replay_text, replay_rect)
        screen.blit(back_text, back_rect)
        
        p.display.flip()
        clock.tick(60)

def animateStalemate(screen, board, clock, lightning_frames, gs, lightning_sound,WIDTH,HEIGHT,IMAGES,SQ_SIZE):
    """Hiệu ứng khi hòa (stalemate)"""
    num_lightning_frames = len(lightning_frames)  # 4 frame
    transition_duration = 30
    fade_duration = 30

    font = p.font.SysFont("Arial", 48, True)
    stalemate_text = font.render("Hòa!", True, p.Color("yellow"))
    stalemate_text_rect = stalemate_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))

    button_font = p.font.SysFont("Arial", 36, True)
    replay_text = button_font.render("Chơi lại", True, p.Color("white"))
    back_text = button_font.render("Quay lại", True, p.Color("white"))
    replay_rect = replay_text.get_rect(center=(WIDTH // 2 - 100, HEIGHT // 2 + 50))
    back_rect = back_text.get_rect(center=(WIDTH // 2 + 100, HEIGHT // 2 + 50))

    temp_board = [row[:] for row in board]
    temp_board[gs.white_king_location[0]][gs.white_king_location[1]] = "--"
    temp_board[gs.black_king_location[0]][gs.black_king_location[1]] = "--"

    white_start_x = gs.white_king_location[1] * SQ_SIZE + SQ_SIZE // 2
    white_start_y = gs.white_king_location[0] * SQ_SIZE + SQ_SIZE // 2
    black_start_x = gs.black_king_location[1] * SQ_SIZE + SQ_SIZE // 2
    black_start_y = gs.black_king_location[0] * SQ_SIZE + SQ_SIZE // 2

    white_target_x = WIDTH // 4
    white_target_y = HEIGHT // 4
    black_target_x = WIDTH * 3 // 4
    black_target_y = HEIGHT // 4

    white_dx = (white_target_x - white_start_x) / transition_duration
    white_dy = (white_target_y - white_start_y) / transition_duration
    black_dx = (black_target_x - black_start_x) / transition_duration
    black_dy = (black_target_y - black_start_y) / transition_duration

    # 1. Phóng to và di chuyển hai quân vua
    for frame in range(transition_duration):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        
        scale_factor = 1 + frame * 1 / transition_duration
        white_king_img = p.transform.scale(IMAGES["wK"], 
                                          (int(SQ_SIZE * scale_factor), int(SQ_SIZE * scale_factor)))
        black_king_img = p.transform.scale(IMAGES["bK"], 
                                          (int(SQ_SIZE * scale_factor), int(SQ_SIZE * scale_factor)))
        
        white_king_x = white_start_x + white_dx * frame - white_king_img.get_width() // 2
        white_king_y = white_start_y + white_dy * frame - white_king_img.get_height() // 2
        black_king_x = black_start_x + black_dx * frame - black_king_img.get_width() // 2
        black_king_y = black_start_y + black_dy * frame - black_king_img.get_height() // 2
        
        screen.blit(white_king_img, (white_king_x, white_king_y))
        screen.blit(black_king_img, (black_king_x, black_king_y))
        
        p.display.flip()
        clock.tick(60)

    # 2. Làm mờ màn hình (không che quân vua) và hiển thị văn bản + nút
    for frame in range(fade_duration):
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        
        alpha = int(100 * frame / fade_duration)
        overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
        overlay.fill((50, 50, 50, alpha))
        screen.blit(overlay, (0, 0))
        
        scale_factor = 2
        white_king_img = p.transform.scale(IMAGES["wK"], (int(SQ_SIZE * scale_factor), int(SQ_SIZE * scale_factor)))
        black_king_img = p.transform.scale(IMAGES["bK"], (int(SQ_SIZE * scale_factor), int(SQ_SIZE * scale_factor)))
        white_king_x = white_target_x - white_king_img.get_width() // 2
        white_king_y = white_target_y - white_king_img.get_height() // 2
        black_king_x = black_target_x - black_king_img.get_width() // 2
        black_king_y = black_target_y - black_king_img.get_height() // 2
        
        screen.blit(stalemate_text, stalemate_text_rect)
        p.draw.rect(screen, p.Color("gray"), replay_rect.inflate(20, 10))
        p.draw.rect(screen, p.Color("gray"), back_rect.inflate(20, 10))
        screen.blit(replay_text, replay_rect)
        screen.blit(back_text, back_rect)
        
        screen.blit(white_king_img, (white_king_x, white_king_y))
        screen.blit(black_king_img, (black_king_x, black_king_y))
        
        p.display.flip()
        clock.tick(60)

    # 3. Vòng lặp chờ với tia sét và âm thanh 10 giây lặp liên tục
    lightning_sound.set_volume(0.3)
    lightning_sound.play(loops=-1)  # Lặp vô hạn
    frame_count = 0
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                lightning_sound.stop()
                return "quit"
            elif e.type == p.MOUSEBUTTONDOWN:
                pos = p.mouse.get_pos()
                if replay_rect.collidepoint(pos):
                    lightning_sound.stop()
                    return "replay"
                elif back_rect.collidepoint(pos):
                    lightning_sound.stop()
                    return "back"
        
        drawBoard(screen, (), [], SQ_SIZE)
        drawPieces(screen, temp_board, IMAGES, SQ_SIZE)
        
        overlay = p.Surface((WIDTH, HEIGHT), p.SRCALPHA)
        overlay.fill((50, 50, 50, 100))
        screen.blit(overlay, (0, 0))
        
        white_king_img = p.transform.scale(IMAGES["wK"], (int(SQ_SIZE * 2), int(SQ_SIZE * 2)))
        black_king_img = p.transform.scale(IMAGES["bK"], (int(SQ_SIZE * 2), int(SQ_SIZE * 2)))
        white_king_x = white_target_x - white_king_img.get_width() // 2
        white_king_y = white_target_y - white_king_img.get_height() // 2
        black_king_x = black_target_x - black_king_img.get_width() // 2
        black_king_y = black_target_y - black_king_img.get_height() // 2
        
        lightning_idx = (frame_count // 5) % num_lightning_frames  # 4 frame, chu kỳ 0.33 giây
        lightning_img = p.transform.scale(lightning_frames[lightning_idx], (WIDTH // 2, SQ_SIZE * 2))
        lightning_x = WIDTH // 4 + (WIDTH // 2 - lightning_img.get_width()) // 2
        lightning_y = HEIGHT // 4 - lightning_img.get_height() // 2
        
        screen.blit(lightning_img, (lightning_x, lightning_y))
        screen.blit(stalemate_text, stalemate_text_rect)
        p.draw.rect(screen, p.Color("gray"), replay_rect.inflate(20, 10))
        p.draw.rect(screen, p.Color("gray"), back_rect.inflate(20, 10))
        screen.blit(replay_text, replay_rect)
        screen.blit(back_text, back_rect)
        
        screen.blit(white_king_img, (white_king_x, white_king_y))
        screen.blit(black_king_img, (black_king_x, black_king_y))
        
        p.display.flip()
        clock.tick(60)
        frame_count += 1