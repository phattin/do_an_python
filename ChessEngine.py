class Move:
    """Lớp đại diện cho một nước đi trong cờ vua"""
    def __init__(self, startSq, endSq, board):
        # Vị trí bắt đầu của nước đi (hàng, cột)
        self.startRow = startSq[0]  # Hàng bắt đầu
        self.startCol = startSq[1]  # Cột bắt đầu
        # Vị trí kết thúc của nước đi (hàng, cột)
        self.endRow = endSq[0]      # Hàng kết thúc
        self.endCol = endSq[1]      # Cột kết thúc
        # Quân cờ được di chuyển (ví dụ: "wK" là vua trắng, "bp" là tốt đen)
        self.pieceMoved = board[self.startRow][self.startCol]
        # Quân cờ bị bắt ở vị trí kết thúc (nếu có, nếu không thì là "--")
        self.pieceCaptured = board[self.endRow][self.endCol]


class GameState:
    """Lớp quản lý trạng thái của ván cờ vua"""
    def __init__(self):
        # Khởi tạo bàn cờ 8x8 với vị trí ban đầu của các quân cờ
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],  # Hàng 0: quân đen (xe, mã, tượng, hậu, vua, ...)
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],  # Hàng 1: tốt đen
            ["--", "--", "--", "--", "--", "--", "--", "--"],  # Hàng 2-5: ô trống
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],  # Hàng 6: tốt trắng
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]   # Hàng 7: quân trắng
        ]
        # Lượt chơi: True nếu trắng đi, False nếu đen đi
        self.white_to_move = True
        # Danh sách lưu lịch sử các nước đi
        self.move_log = []
        # Vị trí ban đầu của vua trắng (hàng 7, cột 4)
        self.white_king_location = (7, 4)
        # Vị trí ban đầu của vua đen (hàng 0, cột 4)
        self.black_king_location = (0, 4)
        # Trạng thái chiếu hết (kết thúc ván, một bên thua)
        self.checkmate = False
        # Trạng thái hòa (không bên nào thắng, không còn nước đi hợp lệ)
        self.stalemate = False
        # Trạng thái vua đang bị chiếu
        self.in_check = False
        # Danh sách các quân bị ghim (pin) - không thể di chuyển tự do
        self.pins = []
        # Danh sách các nước chiếu (check) - vua đang bị tấn công
        self.checks = []
        # Vị trí có thể bắt tốt qua đường (en passant), None nếu không có
        self.enpassant_possible = None
        # Lịch sử các vị trí en passant
        self.enpassant_possible_log = [self.enpassant_possible]
        # Quyền nhập thành (castling) cho trắng và đen
        self.current_castling_rights = {
            "w": {"kingside": True, "queenside": True},  # Trắng: nhập thành gần/xa
            "b": {"kingside": True, "queenside": True}   # Đen: nhập thành gần/xa
        }

    def makeMove(self, move):
        """Thực hiện một nước đi trên bàn cờ"""
        # Xóa quân cờ ở vị trí bắt đầu (đặt thành ô trống "--")
        self.board[move.startRow][move.startCol] = "--"
        # Đặt quân cờ vào vị trí kết thúc
        self.board[move.endRow][move.endCol] = move.pieceMoved
        # Thêm nước(Book) nước đi vào lịch sử
        self.move_log.append(move)
        # Đổi lượt chơi (trắng -> đen hoặc ngược lại)
        self.white_to_move = not self.white_to_move

        # Cập nhật vị trí vua và quyền nhập thành khi vua di chuyển
        if move.pieceMoved == "wK":  # Vua trắng di chuyển
            self.white_king_location = (move.endRow, move.endCol)
            self.current_castling_rights["w"]["kingside"] = False  # Mất quyền nhập thành gần
            self.current_castling_rights["w"]["queenside"] = False  # Mất quyền nhập thành xa
        elif move.pieceMoved == "bK":  # Vua đen di chuyển
            self.black_king_location = (move.endRow, move.endCol)
            self.current_castling_rights["b"]["kingside"] = False
            self.current_castling_rights["b"]["queenside"] = False

        # Cập nhật quyền nhập thành khi xe di chuyển
        if move.pieceMoved == "wR":  # Xe trắng di chuyển
            if move.startRow == 7 and move.startCol == 0:  # Xe ở góc trái
                self.current_castling_rights["w"]["queenside"] = False
            elif move.startRow == 7 and move.startCol == 7:  # Xe ở góc phải
                self.current_castling_rights["w"]["kingside"] = False
        elif move.pieceMoved == "bR":  # Xe đen di chuyển
            if move.startRow == 0 and move.startCol == 0:  # Xe ở góc trái
                self.current_castling_rights["b"]["queenside"] = False
            elif move.startRow == 0 and move.startCol == 7:  # Xe ở góc phải
                self.current_castling_rights["b"]["kingside"] = False

        # Xử lý nước đi bắt tốt qua đường (en passant)
        if move.pieceMoved.endswith("p"):  # Nếu là tốt
            if move.startCol != move.endCol and move.pieceCaptured == "--":  # Bắt chéo mà không có quân ở đích
                if move.pieceMoved.startswith("w") and move.startRow == 3 and move.endRow == 2:  # Tốt trắng
                    if self.enpassant_possible == (move.endRow, move.endCol):
                        self.board[move.startRow][move.endCol] = "--"  # Xóa tốt bị bắt
                elif move.pieceMoved.startswith("b") and move.startRow == 4 and move.endRow == 5:  # Tốt đen
                    if self.enpassant_possible == (move.endRow, move.endCol):
                        self.board[move.startRow][move.endCol] = "--"  # Xóa tốt bị bắt

        # Cập nhật khả năng bắt tốt qua đường
        if move.pieceMoved.endswith("p") and abs(move.startRow - move.endRow) == 2:  # Tốt đi 2 ô
            self.enpassant_possible = ((move.startRow + move.endRow) // 2, move.startCol)  # Vị trí giữa
        else:
            self.enpassant_possible = None  # Không có khả năng bắt qua đường
        self.enpassant_possible_log.append(self.enpassant_possible)  # Lưu vào lịch sử

        # Xử lý nhập thành (castling)
        if move.pieceMoved.endswith("K") and abs(move.startCol - move.endCol) == 2:  # Vua di chuyển 2 ô
            if move.endCol == 6:  # Nhập thành gần
                self.board[move.startRow][7] = "--"  # Xóa xe ở góc
                self.board[move.startRow][5] = move.pieceMoved[0] + "R"  # Đặt xe cạnh vua
            elif move.endCol == 2:  # Nhập thành xa
                self.board[move.startRow][0] = "--"  # Xóa xe ở góc
                self.board[move.startRow][3] = move.pieceMoved[0] + "R"  # Đặt xe cạnh vua

        # Kiểm tra chiếu, ghim và cập nhật trạng thái
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()
        color = "w" if self.white_to_move else "b"  # Xác định bên đang chơi
        if self.isCheckmate(color):  # Kiểm tra chiếu hết
            self.checkmate = True
        elif self.isStalemate(color):  # Kiểm tra hòa
            self.stalemate = True
        else:  # Không chiếu hết cũng không hòa
            self.checkmate = False
            self.stalemate = False

    def undoMove(self):
        """Hoàn tác nước đi cuối cùng"""
        if not self.move_log:  # Nếu không có nước đi nào
            return
        move = self.move_log.pop()  # Lấy nước đi cuối và xóa khỏi lịch sử
        # Đặt lại quân cờ về vị trí ban đầu
        self.board[move.startRow][move.startCol] = move.pieceMoved
        self.board[move.endRow][move.endCol] = move.pieceCaptured
        # Đổi lại lượt chơi
        self.white_to_move = not self.white_to_move

        # Khôi phục vị trí vua
        if move.pieceMoved == "wK":
            self.white_king_location = (move.startRow, move.startCol)
        elif move.pieceMoved == "bK":
            self.black_king_location = (move.startRow, move.startCol)

        # Khôi phục trạng thái bắt tốt qua đường
        self.enpassant_possible_log.pop()
        self.enpassant_possible = self.enpassant_possible_log[-1]

        # Hoàn tác bắt tốt qua đường
        if move.pieceMoved.endswith("p") and move.startCol != move.endCol and move.pieceCaptured == "--":
            if move.pieceMoved.startswith("w") and move.endRow == 2:  # Tốt trắng
                self.board[3][move.endCol] = "bp"  # Đặt lại tốt đen bị bắt
            elif move.pieceMoved.startswith("b") and move.endRow == 5:  # Tốt đen
                self.board[4][move.endCol] = "wp"  # Đặt lại tốt trắng bị bắt

        # Hoàn tác nhập thành
        if move.pieceMoved.endswith("K") and abs(move.startCol - move.endCol) == 2:
            if move.endCol == 6:  # Nhập thành gần
                self.board[move.startRow][5] = "--"  # Xóa xe ở vị trí mới
                self.board[move.startRow][7] = move.pieceMoved[0] + "R"  # Đặt lại xe
            elif move.endCol == 2:  # Nhập thành xa
                self.board[move.startRow][3] = "--"  # Xóa xe ở vị trí mới
                self.board[move.startRow][0] = move.pieceMoved[0] + "R"  # Đặt lại xe

    def checkBasicMove(self, move):
        """Kiểm tra nước đi cơ bản có hợp lệ không (không tính chiếu/ghim)"""
        # Không thể di chuyển ô trống hoặc không di chuyển
        if move.pieceMoved == "--" or (move.startRow == move.endRow and move.startCol == move.endCol):
            return False
        
        # Không thể bắt quân cùng màu
        target_piece = self.board[move.endRow][move.endCol]
        if move.pieceMoved[0] == target_piece[0] and target_piece != "--":
            return False

        # Kiểm tra theo từng loại quân
        if move.pieceMoved.endswith("R"):  # Xe
            return (move.startRow == move.endRow or move.startCol == move.endCol) and self.clearPath(move)  # Đi thẳng và không bị cản
        if move.pieceMoved.endswith("B"):  # Tượng
            return abs(move.startRow - move.endRow) == abs(move.startCol - move.endCol) and self.clearPath(move)  # Đi chéo và không bị cản
        if move.pieceMoved.endswith("Q"):  # Hậu
            return ((move.startRow == move.endRow or move.startCol == move.endCol) or 
                    abs(move.startRow - move.endRow) == abs(move.startCol - move.endCol)) and self.clearPath(move)  # Đi thẳng hoặc chéo
        if move.pieceMoved.endswith("N"):  # Mã
            return (abs(move.startRow - move.endRow), abs(move.startCol - move.endCol)) in [(2, 1), (1, 2)]  # Đi hình chữ L
        if move.pieceMoved.endswith("K"):  # Vua
            if abs(move.startRow - move.endRow) <= 1 and abs(move.startCol - move.endCol) <= 1:  # Đi 1 ô
                return True
            if move.startRow == move.endRow and move.startCol == 4:  # Nhập thành
                color = move.pieceMoved[0]
                if move.endCol == 6 and self.current_castling_rights[color]["kingside"]:  # Nhập thành gần
                    return self.board[move.startRow][5] == "--" and self.board[move.startRow][6] == "--"  # Không bị cản
                if move.endCol == 2 and self.current_castling_rights[color]["queenside"]:  # Nhập thành xa
                    return self.board[move.startRow][1] == "--" and self.board[move.startRow][2] == "--" and self.board[move.startRow][3] == "--"
        if move.pieceMoved.endswith("p"):  # Tốt
            if move.pieceMoved.startswith("w"):  # Tốt trắng
                if move.startCol == move.endCol:  # Đi thẳng
                    if move.startRow - move.endRow == 1 and target_piece == "--":  # Đi 1 ô
                        return True
                    if move.startRow == 6 and move.endRow == 4 and self.board[5][move.endCol] == "--" and target_piece == "--":  # Đi 2 ô từ hàng đầu
                        return True
                elif abs(move.startCol - move.endCol) == 1 and move.startRow - move.endRow == 1:  # Bắt chéo
                    return target_piece.startswith("b") or (move.startRow == 3 and self.enpassant_possible == (move.endRow, move.endCol))
            else:  # Tốt đen
                if move.startCol == move.endCol:  # Đi thẳng
                    if move.endRow - move.startRow == 1 and target_piece == "--":  # Đi 1 ô
                        return True
                    if move.startRow == 1 and move.endRow == 3 and self.board[2][move.endCol] == "--" and target_piece == "--":  # Đi 2 ô từ hàng đầu
                        return True
                elif abs(move.startCol - move.endCol) == 1 and move.endRow - move.startRow == 1:  # Bắt chéo
                    return target_piece.startswith("w") or (move.startRow == 4 and self.enpassant_possible == (move.endRow, move.endCol))
        return False

    def checkMove(self, move):
        """Kiểm tra nước đi có hợp lệ không (bao gồm chiếu và ghim)"""
        # Kiểm tra nước đi cơ bản trước
        if not self.checkBasicMove(move):
            return False

        # Nếu không phải vua, kiểm tra ghim
        if not move.pieceMoved.endswith("K"):
            in_check, pins, checks = self.checkForPinsAndChecks()
            for pin in pins:  # Với mỗi quân bị ghim
                if (move.startRow, move.startCol) == (pin[0], pin[1]):  # Nếu quân di chuyển bị ghim
                    move_dir = (move.endRow - move.startRow, move.endCol - move.startCol)  # Hướng di chuyển
                    pin_dir = (pin[2], pin[3])  # Hướng ghim
                    if move_dir[0] != 0 or move_dir[1] != 0:  # Nếu di chuyển
                        move_dir = (move_dir[0] // abs(move_dir[0]) if move_dir[0] else 0,
                                   move_dir[1] // abs(move_dir[1]) if move_dir[1] else 0)  # Chuẩn hóa hướng
                    if move_dir != pin_dir and move_dir != (-pin_dir[0], -pin_dir[1]):  # Nếu không cùng hướng ghim
                        return False

        # Thử di chuyển tạm thời để kiểm tra chiếu
        original_board = [row[:] for row in self.board]  # Sao lưu bàn cờ
        original_king_loc = self.white_king_location if move.pieceMoved.startswith("w") else self.black_king_location
        self.board[move.startRow][move.startCol] = "--"  # Di chuyển tạm
        self.board[move.endRow][move.endCol] = move.pieceMoved
        if move.pieceMoved.endswith("K"):  # Nếu là vua
            if move.pieceMoved.startswith("w"):
                self.white_king_location = (move.endRow, move.endCol)
            else:
                self.black_king_location = (move.endRow, move.endCol)
        
        in_check, _, _ = self.checkForPinsAndChecks()  # Kiểm tra chiếu sau khi di chuyển
        self.board = original_board  # Khôi phục bàn cờ
        if move.pieceMoved.startswith("w"):  # Khôi phục vị trí vua
            self.white_king_location = original_king_loc
        else:
            self.black_king_location = original_king_loc
        
        return not in_check  # Hợp lệ nếu không bị chiếu

    def wayToMove(self, move):
        """Trả về danh sách các ô có thể đi tới từ vị trí hiện tại"""
        way = []  # Danh sách các ô đích
        r, c = move.startRow, move.startCol  # Vị trí bắt đầu
        color = move.pieceMoved[0]  # Màu quân cờ

        # Xe hoặc Hậu (đi thẳng)
        if move.pieceMoved.endswith("R") or move.pieceMoved.endswith("Q"):
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
            for dr, dc in directions:
                for i in range(1, 8):  # Tối đa 7 ô
                    nr, nc = r + dr * i, c + dc * i  # Vị trí mới
                    if 0 <= nr < 8 and 0 <= nc < 8:  # Trong bàn cờ
                        if self.board[nr][nc] == "--":  # Ô trống
                            way.append((nr, nc))
                        elif self.board[nr][nc][0] != color:  # Quân đối phương
                            way.append((nr, nc))
                            break
                        else:  # Quân cùng màu
                            break
                    else:
                        break

        # Tượng hoặc Hậu (đi chéo)
        if move.pieceMoved.endswith("B") or move.pieceMoved.endswith("Q"):
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # 4 hướng chéo
            for dr, dc in directions:
                for i in range(1, 8):
                    nr, nc = r + dr * i, c + dc * i
                    if 0 <= nr < 8 and 0 <= nc < 8:
                        if self.board[nr][nc] == "--":
                            way.append((nr, nc))
                        elif self.board[nr][nc][0] != color:
                            way.append((nr, nc))
                            break
                        else:
                            break
                    else:
                        break

        # Mã (đi hình chữ L)
        if move.pieceMoved.endswith("N"):
            moves = [(r+2, c+1), (r+2, c-1), (r-2, c+1), (r-2, c-1),
                    (r+1, c+2), (r+1, c-2), (r-1, c+2), (r-1, c-2)]  # 8 vị trí có thể
            for nr, nc in moves:
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == "--" or self.board[nr][nc][0] != color:
                        way.append((nr, nc))

        # Vua (đi 1 ô xung quanh)
        if move.pieceMoved.endswith("K"):
            moves = [(r+1, c), (r-1, c), (r, c+1), (r, c-1),
                    (r+1, c+1), (r+1, c-1), (r-1, c+1), (r-1, c-1)]  # 8 hướng
            for nr, nc in moves:
                if 0 <= nr < 8 and 0 <= nc < 8:
                    if self.board[nr][nc] == "--" or self.board[nr][nc][0] != color:
                        way.append((nr, nc))

        # Tốt
        if move.pieceMoved.endswith("p"):
            direction = -1 if color == "w" else 1  # Trắng đi lên (-1), đen đi xuống (1)
            start_row = 6 if color == "w" else 1  # Hàng bắt đầu
            end_row = r + direction  # Ô phía trước
            if 0 <= end_row < 8:
                if self.board[end_row][c] == "--":  # Ô trống phía trước
                    way.append((end_row, c))
                    if r == start_row and self.board[r + 2 * direction][c] == "--":  # Đi 2 ô từ hàng đầu
                        way.append((r + 2 * direction, c))
                for dc in [-1, 1]:  # Bắt chéo trái/phải
                    if 0 <= c + dc < 8:
                        target = self.board[end_row][c + dc]
                        if target != "--" and target[0] != color:  # Quân đối phương
                            way.append((end_row, c + dc))
                        elif target == "--" and self.enpassant_possible == (end_row, c + dc):  # Bắt qua đường
                            if (color == "w" and r == 3) or (color == "b" and r == 4):
                                way.append((end_row, c + dc))

        return way

    def clearPath(self, move):
        """Kiểm tra đường đi có bị cản không"""
        if move.pieceMoved.endswith("N") or move.pieceMoved.endswith("K"):  # Mã và Vua không cần kiểm tra
            return True
        # Tính bước di chuyển theo hàng và cột
        row_step = 0 if move.startRow == move.endRow else (move.endRow - move.startRow) // abs(move.endRow - move.startRow)
        col_step = 0 if move.startCol == move.endCol else (move.endCol - move.startCol) // abs(move.endCol - move.startCol)
        r, c = move.startRow + row_step, move.startCol + col_step  # Ô tiếp theo
        while (r, c) != (move.endRow, move.endCol):  # Kiểm tra từng ô trên đường
            if self.board[r][c] != "--":  # Có quân cản
                return False
            r += row_step
            c += col_step
        return True

    def getAllMoves(self, color=None):
        """Lấy tất cả nước đi có thể của một bên"""
        moves = []  # Danh sách các nước đi
        current_color = "w" if self.white_to_move else "b"  # Màu hiện tại
        target_color = color if color else current_color  # Màu cần lấy nước đi
        for r in range(8):  # Duyệt qua từng ô
            for c in range(8):
                piece = self.board[r][c]
                if piece != "--" and piece[0] == target_color:  # Nếu là quân của bên cần lấy
                    temp_move = Move((r, c), (r, c), self.board)  # Tạo nước đi tạm
                    possible_moves = self.wayToMove(temp_move)  # Lấy các ô có thể đi
                    for end_pos in possible_moves:
                        move = Move((r, c), end_pos, self.board)  # Tạo nước đi
                        if self.checkBasicMove(move):  # Kiểm tra cơ bản
                            moves.append(move)
        return moves

    def checkForPinsAndChecks(self):
        """Kiểm tra chiếu và ghim"""
        pins = []  # Danh sách ghim
        checks = []  # Danh sách chiếu
        in_check = False  # Trạng thái chiếu
        # Xác định màu quân và vị trí vua
        if self.white_to_move:
            enemy_color, ally_color = "b", "w"
            start_row, start_col = self.white_king_location
        else:
            enemy_color, ally_color = "w", "b"
            start_row, start_col = self.black_king_location

        # Kiểm tra 8 hướng (thẳng và chéo)
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j, (dr, dc) in enumerate(directions):
            possible_pin = ()  # Quân có thể bị ghim
            for i in range(1, 8):  # Tối đa 7 ô
                end_row, end_col = start_row + dr * i, start_col + dc * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece[0] == ally_color and end_piece[1] != "K":  # Quân đồng minh (không phải vua)
                        if not possible_pin:  # Nếu chưa có ghim
                            possible_pin = (end_row, end_col, dr, dc)
                        else:
                            break  # Đã có 2 quân đồng minh, không ghim
                    elif end_piece[0] == enemy_color:  # Quân đối phương
                        enemy_type = end_piece[1]
                        # Kiểm tra quân có thể chiếu hoặc ghim
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or \
                           (enemy_type == "Q") or (i == 1 and enemy_type == "K") or \
                           (i == 1 and enemy_type == "p" and ((enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))):
                            if not possible_pin:  # Không có quân đồng minh giữa vua và quân địch
                                in_check = True
                                checks.append((end_row, end_col, dr, dc))
                                break
                            else:  # Có quân đồng minh bị ghim
                                pins.append(possible_pin)
                                break
                        else:
                            break  # Quân không thể chiếu hoặc ghim
                else:
                    break

        # Kiểm tra chiếu bởi mã
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for dr, dc in knight_moves:
            end_row, end_col = start_row + dr, start_col + dc
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                if self.board[end_row][end_col] == enemy_color + "N":  # Mã đối phương
                    in_check = True
                    checks.append((end_row, end_col, dr, dc))

        return in_check, pins, checks

    def isCheckmate(self, color):
        """Kiểm tra có phải chiếu hết không"""
        king_row, king_col = self.white_king_location if color == "w" else self.black_king_location
        if not self.squareUnderAttack(king_row, king_col, color):  # Vua không bị chiếu
            return False
        return len(self.getAllValidMoves(color)) == 0  # Không còn nước đi hợp lệ

    def isStalemate(self, color):
        """Kiểm tra có phải hòa không"""
        king_row, king_col = self.white_king_location if color == "w" else self.black_king_location
        if self.squareUnderAttack(king_row, king_col, color):  # Vua bị chiếu
            return False
        return len(self.getAllValidMoves(color)) == 0  # Không còn nước đi hợp lệ

    def getAllValidMoves(self, color):
        """Lấy tất cả nước đi hợp lệ của một bên"""
        moves = []
        all_moves = self.getAllMoves(color)  # Lấy tất cả nước đi có thể
        for move in all_moves:
            if self.checkMove(move):  # Kiểm tra hợp lệ (bao gồm chiếu)
                moves.append(move)
        return moves

    def squareUnderAttack(self, row, col, color):
        """Kiểm tra ô có bị tấn công bởi đối phương không"""
        enemy_color = "b" if color == "w" else "w"  # Màu đối phương
        self.white_to_move = not self.white_to_move  # Đổi lượt tạm thời
        opponent_moves = self.getAllMoves(enemy_color)  # Lấy nước đi của đối phương
        self.white_to_move = not self.white_to_move  # Đổi lại lượt
        return any(move.endRow == row and move.endCol == col for move in opponent_moves)  # Ô bị tấn công