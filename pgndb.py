
import os
import os.path
import pgnfx

def count(pgndb):
    i = 0
    with open(pgndb, 'rt') as f:
        for line in f:
            if '[Event' in line:
                i += 1
    return i

def white_wins(pgndb):
    i = 0
    with open(pgndb, 'rt') as f:
        for line in f:
            if '[Result' in line and '1-0' in line:
                i += 1
    return i

def black_wins(pgndb):
    i = 0
    with open(pgndb, 'rt') as f:
        for line in f:
            if '[Result' in line and '0-1' in line:
                i += 1
    return i

def draws(pgndb):
    i = 0
    with open(pgndb, 'rt') as f:
        for line in f:
            if '[Result' in line and '1/2-1/2' in line:
                i += 1
    return i

def prepare_root(root):
    # create children.pgn from raw.pgn
    # sanitize pgns (CURRENTLY DISABLED)
    # make root-level report.csv
    
    if os.path.isfile(root + '/children.pgn'):
        os.remove(root + '/children.pgn')
    
    games = 0
    ww = 0
    bw = 0
    buffer = []
    with open(root + '/raw.pgn', 'rt') as f:
        pgn = f.readline()
        for line in f:
            if not '[Event' in line:
                pgn += line
            else:
                pgn = pgnfx.sanitize(pgn)
                games += 1
                result = pgnfx.result(pgn)
                if result == '1-0':
                    ww += 1
                elif result == '0-1':
                    bw += 1
                buffer.append(pgn)
                pgn = line
                if len(buffer) > 50000:
                    with open(root + '/children.pgn', 'a+') as f:
                        for pgn in buffer:
                            f.write(pgn)
                    buffer = []
                    
    # process the last pgn
    games += 1
    result = pgnfx.result(pgn)
    if result == '1-0':
        ww += 1
    elif result == '0-1':
        bw += 1
    buffer.append(pgn)
        
    # write the buffer to file after looping complete
    with open(root + '/children.pgn', 'a+') as f:
        for pgn in buffer:
            f.write(pgn)
        
    # create root report
    rptstr = 'parent moves,\n' + \
             'fen,rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1\n' + \
             'games,' + str(games) + '\n' + \
             'percent,100\n' + \
             'local percent,100\n' + \
             'white wins,' + str(ww) + '\n' + \
             'black wins,' + str(bw) + '\n'
    with open(root + '/report.csv', 'w') as f:
        f.write(rptstr)

def join(f1, f2):
    # f2 will be appended to f1
    with open(f2, 'rt') as f:
        tmpstr = '\n'
        i = 0
        for line in f:
            tmpstr += line
            i += 1
            if i > 10000:
                with open(f1, 'a') as g:
                    g.write(tmpstr)
                tmpstr = ''
                i = 0
    with open(f1, 'a') as g:
        g.write(tmpstr)

def ispgn(path):
    if os.path.isfile(path) and path[-4:] == '.pgn':
        return True
    else:
        return False 
                