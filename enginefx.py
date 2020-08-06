import chess
import chess.engine

samplefen = 'r1bq1rk1/ppp1ppbp/2np1np1/8/2PP4/1P1BPN2/P4PPP/RNBQK2R w KQ - 3 7'

def get_eval(fen, sec):
    
    # The return value can be processed like this:
    #
    # x = get_eval(blah blah)
    #
    # if x.is_mate():
    #     x.mate() <-- integer with num moves to mate (negative if black to mate)
    # else:
    #     x.cp <-- integer with centipawn eval of position (negative if black is favored)
    
    engine = chess.engine.SimpleEngine.popen_uci('stockfish_20011801_x64_modern.exe')
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(time = sec))
    engine.quit()
    return info

