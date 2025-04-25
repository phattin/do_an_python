import pygame as p
import ChessEngine
from animations import (
    animateMoveKnight, animateMovePawn, animateMoveRook, animateMoveBishop, animatetransfer, animateCheckmate, animateStalemate,animateMoveKing,animateMoveQueen
)
from move_history import MoveHistoryWindow
import chess
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, List, Dict
import random
import pickle
import os

# Constants
MARGIN = 20
WIDTH = HEIGHT = 650
INFO_WIDTH = 150
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
screen = p.display.set_mode((WIDTH + MARGIN + INFO_WIDTH, HEIGHT + MARGIN))

# Mã hóa bàn cờ cho AI
def board_to_input(board: chess.Board) -> np.ndarray:
    """
    Chuyển trạng thái bàn cờ thành ma trận 12x8x8 (12 lớp cho 6 loại quân x 2 màu).
    """
    board_array = np.zeros((12, 8, 8), dtype=np.float32)
    piece_map = {
        chess.PAWN: 0, chess.KNIGHT: 1, chess.BISHOP: 2,
        chess.ROOK: 3, chess.QUEEN: 4, chess.KING: 5
    }
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            color = piece.color
            piece_type = piece.piece_type
            rank, file = divmod(square, 8)
            channel = piece_map[piece_type] + (6 if color == chess.BLACK else 0)
            board_array[channel, rank, file] = 1
    
    return board_array

# Mạng nơ-ron
class ChessNet(nn.Module):
    def __init__(self):
        super(ChessNet, self).__init__()
        self.conv1 = nn.Conv2d(12, 64, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * 8 * 8, 512)
        self.policy_head = nn.Linear(512, 4096)  # 4096 cho tất cả nước đi
        self.value_head = nn.Linear(512, 1)
        
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(-1, 64 * 8 * 8)
        x = torch.relu(self.fc1(x))
        policy = torch.softmax(self.policy_head(x), dim=-1)
        value = torch.tanh(self.value_head(x))
        return policy, value

# MCTS Node
class MCTSNode:
    def __init__(self, board: chess.Board, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = {}
        self.visits = 0
        self.value = 0.0
        self.prior = 0.0

# Monte Carlo Tree Search
class MCTS:
    def __init__(self, model: ChessNet, num_simulations: int = 100):
        self.model = model
        self.num_simulations = num_simulations
        self.c_puct = 1.0

    def search(self, board: chess.Board) -> Tuple[chess.Move, np.ndarray, List[chess.Move]]:
        root = MCTSNode(board)
        legal_moves = list(board.legal_moves)
        move_to_index = {move: idx for idx, move in enumerate(legal_moves)}
        
        board_input = torch.tensor(board_to_input(board), dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            policy, _ = self.model(board_input)
        policy = policy.numpy()[0]
        
        for move in legal_moves:
            child_board = board.copy()
            child_board.push(move)
            root.children[move] = MCTSNode(child_board, root, move)
            root.children[move].prior = policy[move_to_index.get(move, 0)]
        
        for _ in range(self.num_simulations):
            node = root
            search_board = board.copy()
            
            while node.children:
                move, node = self.select_child(node)
                search_board.push(move)
            
            if not search_board.is_game_over():
                board_input = torch.tensor(board_to_input(search_board), dtype=torch.float32).unsqueeze(0)
                with torch.no_grad():
                    _, value = self.model(board_input)
                value = value.item()
            else:
                value = 1.0 if search_board.is_checkmate() and search_board.turn == chess.BLACK else \
                       -1.0 if search_board.is_checkmate() else 0.0
            
            while node:
                node.visits += 1
                node.value += value
                node = node.parent
                value = -value
        
        visits = np.array([root.children[move].visits for move in legal_moves])
        policy = visits / visits.sum()
        best_move = legal_moves[np.argmax(visits)]
        return best_move, policy, legal_moves

    def select_child(self, node: MCTSNode) -> Tuple[chess.Move, MCTSNode]:
        best_score = float('-inf')
        best_move = None
        best_child = None
        
        for move, child in node.children.items():
            q = child.value / (child.visits + 1e-6)
            u = self.c_puct * child.prior * np.sqrt(node.visits) / (1 + child.visits)
            score = q + u
            if score > best_score:
                best_score = score
                best_move = move
                best_child = child
        
        return best_move, best_child

# Self-play để huấn luyện
def self_play(model: ChessNet, num_games: int = 5) -> List[Tuple[np.ndarray, np.ndarray, float, List[chess.Move]]]:
    data = []
    mcts = MCTS(model)
    
    for game in range(num_games):
        print(f"Playing self-play game {game + 1}/{num_games}")
        board = chess.Board()
        game_data = []
        
        while not board.is_game_over():
            move, policy, legal_moves = mcts.search(board)
            game_data.append((board_to_input(board), policy, legal_moves))
            board.push(move)
        
        if board.is_checkmate():
            result = 1.0 if board.turn == chess.BLACK else -1.0
        else:
            result = 0.0
        
        for board_input, policy, legal_moves in game_data:
            data.append((board_input, policy, result, legal_moves))
        
    return data

def train_model(model: ChessNet, data: List[Tuple[np.ndarray, np.ndarray, float, List[chess.Move]]], epochs: int = 3):
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    policy_loss_fn = nn.CrossEntropyLoss()
    value_loss_fn = nn.MSELoss()
    
    for epoch in range(epochs):
        total_loss = 0.0
        random.shuffle(data)
        
        for board_input, policy_target, value_target, legal_moves in data:
            board_input = torch.tensor(board_input, dtype=torch.float32).unsqueeze(0)
            policy_target = torch.tensor(policy_target, dtype=torch.float32).unsqueeze(0)  # [1, num_legal_moves]
            value_target = torch.tensor([[value_target]], dtype=torch.float32)  # [1, 1]
            
            optimizer.zero_grad()
            policy, value = model(board_input)
            
            # Lấy xác suất chỉ cho các nước đi hợp lệ
            move_to_index = {move: idx for idx, move in enumerate(legal_moves)}
            legal_indices = [move_to_index[move] for move in legal_moves]
            policy = policy[:, legal_indices]  # [1, num_legal_moves]
            
            policy_loss = policy_loss_fn(policy, policy_target)
            value_loss = value_loss_fn(value, value_target)
            loss = policy_loss + value_loss
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
        
        print(f"Epoch {epoch + 1}, Loss: {total_loss / len(data)}")

# Chuyển đổi từ ChessEngine.GameState sang chess.Board
def game_state_to_chess_board(gs: ChessEngine.GameState) -> chess.Board:
    """
    Chuyển trạng thái bàn cờ từ ChessEngine.GameState sang chess.Board.
    """
    board = chess.Board()
    board.clear()
    
    piece_map = {
        'wp': chess.Piece(chess.PAWN, chess.WHITE),
        'wN': chess.Piece(chess.KNIGHT, chess.WHITE),
        'wB': chess.Piece(chess.BISHOP, chess.WHITE),
        'wR': chess.Piece(chess.ROOK, chess.WHITE),
        'wQ': chess.Piece(chess.QUEEN, chess.WHITE),
        'wK': chess.Piece(chess.KING, chess.WHITE),
        'bp': chess.Piece(chess.PAWN, chess.BLACK),
        'bN': chess.Piece(chess.KNIGHT, chess.BLACK),
        'bB': chess.Piece(chess.BISHOP, chess.BLACK),
        'bR': chess.Piece(chess.ROOK, chess.BLACK),
        'bQ': chess.Piece(chess.QUEEN, chess.BLACK),
        'bK': chess.Piece(chess.KING, chess.BLACK),
        '--': None
    }
    
    for r in range(8):
        for c in range(8):
            piece = gs.board[r][c]
            square = chess.square(c, 7 - r)
            board.set_piece_at(square, piece_map[piece])
    
    board.turn = chess.WHITE if gs.white_to_move else chess.BLACK
    return board

# Chuyển đổi từ chess.Move sang ChessEngine.Move
def chess_move_to_engine_move(chess_move: chess.Move, gs: ChessEngine.GameState) -> ChessEngine.Move:
    """
    Chuyển nước đi từ chess.Move sang ChessEngine.Move.
    """
    start_square = chess_move.from_square
    end_square = chess_move.to_square
    start_row, start_col = 7 - (start_square // 8), start_square % 8
    end_row, end_col = 7 - (end_square // 8), end_square % 8
    move = ChessEngine.Move((start_row, start_col), (end_row, end_col), gs.board)
    
    if chess_move.promotion:
        piece_moved = gs.board[start_row][start_col]
        promotion_map = {
            chess.QUEEN: 'Q',
            chess.ROOK: 'R',
            chess.BISHOP: 'B',
            chess.KNIGHT: 'N'
        }
        move.promoted_to = piece_moved[0] + promotion_map[chess_move.promotion]
    
    return move

# Hàm chọn nước đi của AI
def get_ai_move(gs: ChessEngine.GameState, model: ChessNet, num_simulations: int = 100) -> ChessEngine.Move:
    """
    Trả về nước đi tốt nhất cho AI sử dụng MCTS và mạng nơ-ron.
    """

    board = game_state_to_chess_board(gs)
    mcts = MCTS(model, num_simulations)
    chess_move, _, _ = mcts.search(board)
    return chess_move_to_engine_move(chess_move, gs)

# Load images
def loadImages():
    """Load and scale images for chess pieces and animation effects."""
    pieces = ['wp', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bp', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        try:
            IMAGES[piece] = p.transform.scale(
                p.image.load(f"images/{piece}.png"), (SQ_SIZE, SQ_SIZE)
            )
        except FileNotFoundError:
            print(f"Error: Không tìm thấy images/{piece}.png")
            raise

    fireball_frames = []
    for i in range(1, 61):
        fireball_img = p.transform.scale(
            p.image.load(f"16_sunburn_spritesheet/{i}_16_sunburn_spritesheet.png"),
            (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        fireball_frames.append(fireball_img)
    IMAGES['fireball_frames'] = fireball_frames

    sunboom_frames = []
    num_sunboom_frames = 12
    for i in range(1, num_sunboom_frames + 1):
        sunboom_img = p.transform.scale(
            p.image.load(f"03/{i}_03.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
        )
        sunboom_frames.append(sunboom_img)
    IMAGES['sunboom_frames'] = sunboom_frames


    boom_frames = []
    for i in range(1, 13):
        try:
            boom_img = p.transform.scale(
                p.image.load(f"03/{39+i}_03.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            boom_frames.append(boom_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy 03/{39+i}_03.png")
            raise
    IMAGES['boom_frames'] = boom_frames

    slash_color1_frames = []
    for i in range(1, 10):
        try:
            slash_img = p.transform.scale(
                p.image.load(f"Frames/Slash_color1_frame{i}.png"), (SQ_SIZE * 3, SQ_SIZE * 3)
            )
            slash_color1_frames.append(slash_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy Frames/Slash_color1_frame{i}.png")
            raise
    IMAGES['Slash_color1_frame1'] = slash_color1_frames

    p_boom_frames = []
    for i in range(256, 269):
        try:
            p_boom_img = p.transform.scale(
                p.image.load(f"p_smoke/{i}_Smoke.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            p_boom_frames.append(p_boom_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy p_smoke/{i}_Smoke.png")
            raise
    IMAGES['p_boom_frames'] = p_boom_frames

    p_slash_color1_frames = []
    for i in range(1, 11):
        try:
            p_slash_img = p.transform.scale(
                p.image.load(f"p_Frames/warrior_skill1_frame{i}.png"), (SQ_SIZE * 3, SQ_SIZE * 3)
            )
            p_slash_color1_frames.append(p_slash_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy p_Frames/warrior_skill1_frame{i}.png")
            raise
    IMAGES['p_Slash_color1_frame1'] = p_slash_color1_frames

    frost_frames = []
    for i in range(1, 58):
        try:
            frost_img = p.transform.scale(
                p.image.load(f"frost/frost ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            frost_frames.append(frost_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy frost/frost ({i}).png")
            raise
    IMAGES['frost_frames'] = frost_frames

    frostleft_frames = []
    for i in range(1, 47):
        try:
            frostleft_img = p.transform.scale(
                p.image.load(f"frostleft/frostleft ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            frostleft_frames.append(frostleft_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy frostleft/frostleft ({i}).png")
            raise
    IMAGES['frostleft_frames'] = frostleft_frames

    frostright_frames = []
    for i in range(1, 47):
        try:
            frostright_img = p.transform.scale(
                p.image.load(f"frostright/frostrightskill ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            frostright_frames.append(frostright_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy frostright/frostrightskill ({i}).png")
            raise
    IMAGES['frostright_frames'] = frostright_frames

    freeze_frames = []
    for i in range(1, 55):
        try:
            freeze_img = p.transform.scale(
                p.image.load(f"freeze/boom ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            freeze_frames.append(freeze_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy freeze/boom ({i}).png")
            raise
    IMAGES['freeze_frames'] = freeze_frames

    end_boom_frames = []
    end_num_boom_frames = 81
    for i in range(end_num_boom_frames + 1):
        try:
            end_boom_img = p.transform.scale(
                p.image.load(f"endgame_boom/frame00{i:02d}.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            end_boom_frames.append(end_boom_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy endgame_boom/frame00{i:02d}.png")
            raise
    IMAGES['end_boom_frames'] = end_boom_frames

    end_lightning_frames = []
    end_num_lightning_frames = 4
    for i in range(1, end_num_lightning_frames + 1):
        try:
            end_lightning_img = p.transform.scale(
                p.image.load(f"endgame_lightning/lightning_skill1_frame{i}.png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            end_lightning_frames.append(end_lightning_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy endgame_lightning/lightning_skill1_frame{i}.png")
            raise
    IMAGES['end_lightning_frames'] = end_lightning_frames

    magic_frames = []
    for i in range(1, 65):
        try:
            magic_img = p.transform.scale(
                p.image.load(f"b_magic/magic ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            magic_frames.append(magic_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy b_magic/magic ({i}).png")
            raise
    IMAGES['magic_frames'] = magic_frames

    magic_move_frames = []
    for i in range(1, 61):
        try:
            magic_move_img = p.transform.scale(
                p.image.load(f"b_move/move_ ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            magic_move_frames.append(magic_move_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy b_move/move_ ({i}).png")
            raise
    IMAGES['magic_move_frames'] = magic_move_frames

    magic_boom_frames = []
    for i in range(1, 11):
        try:
            magic_boom_img = p.transform.scale(
                p.image.load(f"b_boom/boom_ ({i}).png"), (SQ_SIZE * 3, SQ_SIZE * 3)
            )
            magic_boom_frames.append(magic_boom_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy b_boom/boom_ ({i}).png")
            raise
    IMAGES['magic_boom_frames'] = magic_boom_frames

    transfer_frames = []
    num_transfer_frames = 86
    for i in range(1, num_transfer_frames + 1):
        try:
            transfer_img = p.transform.scale(
                p.image.load(f"transfer/transfer ({i}).png"), (SQ_SIZE * 2, SQ_SIZE * 2)
            )
            transfer_frames.append(transfer_img)
        except FileNotFoundError:
            print(f"Error: Không tìm thấy transfer/transfer ({i}).png")
            raise
    IMAGES['transfer_frames'] = transfer_frames

# Phong cấp cho người chơi
def showPromotionWindow(screen, color):
    choices = ["Q", "R", "B", "N"]
    width, height = 4 * SQ_SIZE, SQ_SIZE
    x = 2 * SQ_SIZE
    y = 3 * SQ_SIZE
    rects = []

    border_rect = p.Rect(x - 4, y - 4, width + 8, height + 8)
    p.draw.rect(screen, p.Color("black"), border_rect, border_radius=5)

    promotion_bg = p.Surface((width, height))
    promotion_bg.fill(p.Color("darkgray"))
    screen.blit(promotion_bg, (x, y))

    inner_border = p.Rect(x, y, width, height)
    p.draw.rect(screen, p.Color("white"), inner_border, 2)

    for i in range(1, 4):
        p.draw.line(screen, p.Color("black"), (x + i * SQ_SIZE, y), (x + i * SQ_SIZE, y + height), 3)

    for i, ch in enumerate(choices):
        piece_code = color + ch
        img = IMAGES[piece_code]
        pos_x = x + i * SQ_SIZE + (SQ_SIZE - img.get_width()) // 2
        pos_y = y + (SQ_SIZE - img.get_height()) // 2
        screen.blit(img, (pos_x, pos_y))
        rects.append((p.Rect(x + i * SQ_SIZE, y, SQ_SIZE, SQ_SIZE), ch))

    p.display.flip()
    while True:
        for e in p.event.get():
            if e.type == p.MOUSEBUTTONDOWN:
                mouse_pos = e.pos
                for rect, ch in rects:
                    if rect.collidepoint(mouse_pos):
                        return ch

# Vẽ bàn cờ
def drawBoard(screen, sqSelected, validMoves, flip=False):
    colors = [p.Color("white"), p.Color("#779556")]
    highlight = p.Color("blue")
    try:
        move_img = p.transform.scale(p.image.load("move.png"), (SQ_SIZE, SQ_SIZE))
    except FileNotFoundError:
        print("Error: Không tìm thấy move.png")
        raise
    
    screen.fill(p.Color("white"))
    font = p.font.SysFont("Arial", 20, True)
    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

    for r in range(DIMENSION):
        for c in range(DIMENSION):
            real_r = r if not flip else DIMENSION - 1 - r
            real_c = c if not flip else DIMENSION - 1 - c
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(MARGIN + c * SQ_SIZE, real_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            if sqSelected == (r, c):
                p.draw.rect(screen, highlight, p.Rect(MARGIN + real_c * SQ_SIZE, real_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            elif (r, c) in validMoves:
                screen.blit(move_img, (MARGIN + real_c * SQ_SIZE, real_r * SQ_SIZE))

            if c == 0:
                label = font.render(ranks[r], True, p.Color("black"))
                screen.blit(label, (5, real_r * SQ_SIZE + 25))
            if r == 7:
                label = font.render(files[c], True, p.Color("black"))
                screen.blit(label, (MARGIN + real_c * SQ_SIZE + SQ_SIZE // 2 - 5, HEIGHT - 5))

# Vẽ quân cờ
def drawPieces(screen, board, flip=False):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            real_r = r if not flip else DIMENSION - 1 - r
            real_c = c if not flip else DIMENSION - 1 - c
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(MARGIN + real_c * SQ_SIZE, real_r * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Vẽ trạng thái trò chơi
def drawGameState(screen, gs, sqSelected, validMoves, flip_board):
    drawBoard(screen, sqSelected, validMoves, flip_board)
    drawPieces(screen, gs.board, flip_board)

# # Vẽ quân cờ bị ăn
# captured_white = []
# captured_black = []

# Hàm vẽ quân cờ bị ăn (giữ nguyên)
def drawCapturedPieces(screen, captured_white, captured_black):
    background_color = p.Color(222, 184, 135)
    p.draw.rect(screen, background_color, p.Rect(HEIGHT + MARGIN, 0, INFO_WIDTH, HEIGHT + MARGIN))
    piece_size = 30
    spacing = 5

    x_offset_black = WIDTH + MARGIN + 20
    y_offset_black = 20
    for i, piece in enumerate(captured_black):
        img = p.transform.scale(IMAGES[piece], (piece_size, piece_size))
        screen.blit(img, (x_offset_black, y_offset_black + i * (piece_size + spacing)))

    x_offset_white = WIDTH + MARGIN + 100
    y_offset_white = 20
    for i, piece in enumerate(captured_white):
        img = p.transform.scale(IMAGES[piece], (piece_size, piece_size))
        screen.blit(img, (x_offset_white, y_offset_white + i * (piece_size + spacing)))

# Hàm chính (thay thế hàm main hiện tại)
# Hàm chính (sửa để AI chơi đen, người chơi trắng, và tiếp tục huấn luyện)
def main(two_player=False):
    p.init()
    print("Khởi tạo Pygame thành công")
    move_window = MoveHistoryWindow()
    p.mixer.init()
    flip_board = False
    i = 1  # Biến kiểm soát lượt (giữ nguyên từ mã của bạn)
    
    move_sound1 = p.mixer.Sound("sounds/chessmove1.wav")
    move_sound2 = p.mixer.Sound("sounds/chessmove2.wav")
    move_sound3 = p.mixer.Sound("sounds/chesscapture.wav")
    endgame_explosion_sound = p.mixer.Sound("sounds/hq-explosion-6288.wav")
    endgame_explosion_sound.set_volume(0.3)
    endgame_lightning_sound = p.mixer.Sound("sounds/electric-sparks-6130.wav")

    # Hiển thị màn hình đang tải
    screen.fill(p.Color("black"))
    font = p.font.SysFont("Arial", 30, True)
    loading_text = font.render("Đang khởi tạo AI...", True, p.Color("white"))
    screen.blit(loading_text, (WIDTH // 2 - loading_text.get_width() // 2, HEIGHT // 2))
    p.display.flip()
    print("Hiển thị màn hình đang tải")

    # Khởi tạo và huấn luyện AI
    model = ChessNet()
    model_path = "chess_model.pth"
    data_path = "chess_data.pkl"
    data = []

    # Tải mô hình nếu tồn tại
    if os.path.exists(model_path):
        model.load_state_dict(torch.load(model_path))
        print("Đã tải mô hình từ chess_model.pth")

    # Tải dữ liệu cũ nếu tồn tại
    if os.path.exists(data_path):
        with open(data_path, 'rb') as f:
            data = pickle.load(f)
        print("Đã tải dữ liệu huấn luyện từ chess_data.pkl")

    # Huấn luyện thêm
    print("Huấn luyện AI...")
    new_data = self_play(model, num_games=5)  # Tạo dữ liệu mới
    data.extend(new_data)  # Kết hợp dữ liệu cũ và mới
    train_model(model, data, epochs=3)  # Huấn luyện trên tất cả dữ liệu
    with open(data_path, 'wb') as f:
        pickle.dump(data, f)
    print("Đã lưu dữ liệu huấn luyện vào chess_data.pkl")
    torch.save(model.state_dict(), model_path)
    print("Đã lưu mô hình vào chess_model.pth")

    clock = p.time.Clock()
    gs = ChessEngine.GameState()
    print("Khởi tạo GameState")
    loadImages()
    print("Tải hình ảnh thành công")

    running = True
    sqSelected = ""
    playerClicks = []
    validMoves = []
    captured_white = []  # Khởi tạo cục bộ
    captured_black = []  # Khởi tạo cục bộ

    while running:
        if not two_player and not gs.white_to_move and not gs.checkmate and not gs.stalemate:
            ai_move = get_ai_move(gs, model)
                       
            if ai_move.pieceCaptured != "--":
                if ai_move.pieceCaptured[0] == 'w':
                    captured_white.append(ai_move.pieceCaptured)
                else:
                    captured_black.append(ai_move.pieceCaptured)
            
            if ai_move.pieceMoved in ["wN", "bN"]:
                animateMoveKnight(
                    ai_move, screen, gs.board, clock,
                    IMAGES['Slash_color1_frame1'], IMAGES['boom_frames'],
                    IMAGES, SQ_SIZE, "lightning"
                )
            elif ai_move.pieceMoved in ["wp", "bp"]:
                animateMovePawn(
                    ai_move, ai_move, screen, gs.board, clock,
                    IMAGES['p_Slash_color1_frame1'], IMAGES['p_boom_frames'],
                    IMAGES, SQ_SIZE, "lightning"
                )
            elif ai_move.pieceMoved in ["wR", "bR"]:
                animateMoveRook(
                    ai_move, screen, gs.board, clock,
                    IMAGES['freeze_frames'], IMAGES['frost_frames'],
                    IMAGES['frostright_frames'], IMAGES['frostleft_frames'],
                    IMAGES, SQ_SIZE
                )
            elif ai_move.pieceMoved in ["wB", "bB"]:
                animateMoveBishop(
                    ai_move, screen, gs.board, clock,
                    IMAGES['magic_frames'], IMAGES['magic_boom_frames'],
                    IMAGES['magic_move_frames'],
                    IMAGES, SQ_SIZE
                )
            elif ai_move.pieceMoved in ["wQ","bQ"]:
                animateMoveQueen(
                    move,screen,gs.board,clock,
                    IMAGES['fireball_frames'],IMAGES['sunboom_frames'],
                    IMAGES,SQ_SIZE
                    )
            elif  ai_move.pieceMoved in ["wK","bK"]:
                animateMoveKing(
                    move,screen,gs.board,clock,
                    IMAGES['thunder_frames'],IMAGES['tdboom_frames'],
                    IMAGES,SQ_SIZE
                    )
            gs.makeMove(ai_move)
            move_window.add_move(ai_move.getFullNotation(), ai_move)
            
            if ai_move.pieceMoved.endswith("p") and ai_move.endRow == 7:  # Phong cấp cho AI (đen)
                promoted_piece = 'Q'  # AI tự chọn Hậu
                gs.board[ai_move.endRow][ai_move.endCol] = ai_move.pieceMoved[0] + promoted_piece
                animatetransfer(ai_move, screen, gs.board, clock, IMAGES['transfer_frames'], 43, 65, IMAGES, SQ_SIZE)
            
            if ai_move.pieceCaptured == "--":
                move_sound2.play()
                i = 3 - i
            else:
                move_sound3.play()
                i = 3 - i
            
            drawGameState(screen, gs, sqSelected, validMoves, flip_board)
            drawCapturedPieces(screen, captured_white, captured_black)
            move_window.update()
            p.display.flip()

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = (location[0] - MARGIN) // SQ_SIZE
                row = location[1] // SQ_SIZE
                if flip_board:
                    row = 7 - row
                    col = 7 - col
                if 0 <= row < 8 and 0 <= col < 8:
                    if sqSelected == (row, col):
                        sqSelected = ""
                        playerClicks = []
                        validMoves = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected)

                        if len(playerClicks) == 1:
                            piece = gs.board[row][col]
                            if gs.white_to_move and piece.startswith("w"):  # Chỉ cho phép chọn quân trắng
                                move = ChessEngine.Move(playerClicks[0], playerClicks[0], gs.board)
                                validMoves = gs.wayToMove(move)
                                move_sound1.play()

                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            if gs.white_to_move and move.pieceMoved.startswith("w") and i==1:  # Kiểm tra quân trắng
                                if gs.checkMove(move):
                                    if move.pieceCaptured != "--":
                                        if move.pieceCaptured[0] == 'w':
                                            captured_white.append(move.pieceCaptured)
                                        else:
                                            captured_black.append(move.pieceCaptured)
                                    if move.pieceMoved in ["wN"]:
                                        animateMoveKnight(
                                            move, screen, gs.board, clock,
                                            IMAGES['Slash_color1_frame1'], IMAGES['boom_frames'],
                                            IMAGES, SQ_SIZE, "lightning"
                                        )
                                    elif move.pieceMoved in ["wp"]:
                                        animateMovePawn(
                                            move, screen, gs.board, clock,
                                            IMAGES['p_Slash_color1_frame1'], IMAGES['p_boom_frames'],
                                            IMAGES, SQ_SIZE, "lightning"
                                        )
                                    elif move.pieceMoved in ["wR"]:
                                        animateMoveRook(
                                            move, screen, gs.board, clock,
                                            IMAGES['freeze_frames'], IMAGES['frost_frames'],
                                            IMAGES['frostright_frames'], IMAGES['frostleft_frames'],
                                            IMAGES, SQ_SIZE
                                        )
                                    elif move.pieceMoved in ["wB"]:
                                        animateMoveBishop(
                                            move, screen, gs.board, clock,
                                            IMAGES['magic_frames'], IMAGES['magic_boom_frames'],
                                            IMAGES['magic_move_frames'],
                                            IMAGES, SQ_SIZE
                                        )
                                    elif move.pieceMoved in ["wQ","bQ"]:
                                        animateMoveQueen(
                                            move,screen,gs.board,clock,
                                            IMAGES['fireball_frames'],IMAGES['sunboom_frames'],
                                            IMAGES,SQ_SIZE
                                        )
                                    elif  move.pieceMoved in ["wK","bK"]:
                                        animateMoveKing(
                                            move,screen,gs.board,clock,
                                            IMAGES['thunder_frames'],IMAGES['tdboom_frames'],
                                            IMAGES,SQ_SIZE
                                        )
                                    gs.makeMove(move)

                                    move_window.add_move(move.getFullNotation(), move)

                                    if move.pieceMoved.endswith("p") and move.endRow == 0:  # Phong cấp cho người chơi (trắng)
                                        drawGameState(screen, gs, None, [], flip_board)
                                        promoted_piece = showPromotionWindow(screen, move.pieceMoved[0])
                                        gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + promoted_piece
                                        if promoted_piece == 'N':
                                            animatetransfer(move, screen, gs.board, clock, IMAGES['transfer_frames'], 1, 21, IMAGES, SQ_SIZE)
                                        elif promoted_piece == 'R':
                                            animatetransfer(move, screen, gs.board, clock, IMAGES['transfer_frames'], 21, 43, IMAGES, SQ_SIZE)
                                        elif promoted_piece == 'Q':
                                            animatetransfer(move, screen, gs.board, clock, IMAGES['transfer_frames'], 43, 65, IMAGES, SQ_SIZE)
                                        elif promoted_piece == 'B':
                                            animatetransfer(move, screen, gs.board, clock, IMAGES['transfer_frames'], 65, 88, IMAGES, SQ_SIZE)
                                    if move.pieceCaptured == "--":
                                        move_sound2.play()
                                        i = 3 - i
                                    else:
                                        move_sound3.play()
                                        i = 3 - i
                                    sqSelected = ""
                                    playerClicks = []
                                    validMoves = []
                                else:
                                    playerClicks = [playerClicks[0]]
                                    sqSelected = playerClicks[0]
                                    move = ChessEngine.Move(playerClicks[0], playerClicks[0], gs.board)
                                    validMoves = gs.wayToMove(move)

        drawGameState(screen, gs, sqSelected, validMoves, flip_board)
        drawCapturedPieces(screen, captured_white, captured_black)

        if gs.checkmate:
            result = animateCheckmate(screen, gs.board, clock, IMAGES['freeze_frames'], IMAGES['end_boom_frames'], gs, endgame_explosion_sound, WIDTH, HEIGHT, IMAGES, SQ_SIZE)
            print("Checkmate! Game over.")
            if result == "replay":
                gs = ChessEngine.GameState()
                sqSelected = ""
                playerClicks = []
                validMoves = []
                captured_white = []
                captured_black = []
            elif result == "back" or result == "quit":
                running = False
        elif gs.stalemate:
            result = animateStalemate(screen, gs.board, clock, IMAGES['end_lightning_frames'], gs, endgame_lightning_sound, WIDTH, HEIGHT, IMAGES, SQ_SIZE)
            print("Stalemate! Game over.")
            if result == "replay":
                gs = ChessEngine.GameState()
                sqSelected = ""
                playerClicks = []
                validMoves = []
                captured_white = []
                captured_black = []
            elif result == "back" or result == "quit":
                running = False
        move_window.update()
        clock.tick(MAX_FPS)
        p.display.flip()
    p.quit()

if __name__ == "__main__":
    main(two_player=True)