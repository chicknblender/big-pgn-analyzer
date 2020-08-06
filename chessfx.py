import chess
import chess.pgn
import io

def make_fen(moves):
    pgn = io.StringIO(moves)
    game = chess.pgn.read_game(pgn)
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
    fen = chess.Board.fen(board)
    return fen