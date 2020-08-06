import pgnfx
import pgndb
import os
import os.path
import chessfx

def get_opening_dir(opening, srcdir, destination_dir):
    
    #remove non-pgn files:
    dirlist = os.listdir(srcdir)
    temp = []
    for item in dirlist:
        if pgndb.ispgn(srcdir + '/' + item):
            temp.append(srcdir + '/' + item)
    dirlist = temp

    print(str(len(dirlist)) + ' PGN files found. Running get_opening on all...')
    for item in dirlist:
        get_opening(opening, item, destination_dir)
    print('get_opening_dir operation complete.')


def get_opening(opening, srcfile, destination_dir):
    
    # only run with previously-sanitized pgndb's!
    
    # opening should be a list of strings that produce chess positions that transpose into each other.
    # Each string must start with ' 1. ' (the space prevents finding e.g. '31. ')
    # Example: [ ' 1. e4 e5 2. d4', 1' 1. d4 e5 2. e4' ]
    
    if not pgndb.ispgn(srcfile):
        print('get_opening error: srcfile is not a pgn: ' + str(srcfile))
        exit()
    
    if not os.path.isdir(destination_dir):
        print("get_opening error: destination_dir does not exist. (given '" + str(destination_dir) + "')")
        exit()
    if os.path.isfile(destination_dir + '/' + srcfile[srcfile.rfind('/')+1:]):
        print("get_opening error: " + destination_dir + '/' + srcfile[srcfile.rfind('/')+1:] + " already exists.")
        exit()
        
    for o in opening:
        if o[:4] != ' 1. ':
            print("get_opening error: opening must start with ' 1. ' (instead given '" + str(o) + "')")
            exit()
        
    if len(opening) > 1:
        o0 = opening[0]
        fen0 = chessfx.make_fen(o0)
        for o in opening[1:]:
            fen = chessfx.make_fen(o)
            if fen != fen0:
                print("get_opening error: opening mismatch found: " + o0 + " does not transpose to " + o)
                exit()
        
    print("opening extraction started from file: " + srcfile)
    gamelist = ''
    g = 0
    
    with open(srcfile, 'rt') as pgn_db:
        pgn = pgn_db.readline()
        for line in pgn_db:
            if '[Event' in line: # then process the current pgn
                pgnmoves = pgnfx.strip_headers(pgn)
                for o in opening:
                    if o in pgnmoves:
                        gamelist += pgn
                        g += 1
                        break
                if g > 10000:
                    with open(destination_dir + '/' + srcfile[srcfile.rfind('/')+1:], 'a+') as f:
                        f.write(gamelist)
                    gamelist = ''
                    g = 0
                pgn = line # reset for the new pgn that just started
                
            else: # then keep building the current pgn
                pgn += line
                
    # process the last pgn which is hanging after the loop:
    pgnmoves = pgnfx.strip_headers(pgn)
    for o in opening:
        if o in pgnmoves:
            gamelist += pgn
            break
    
    # write the remaining games not yet written:
    with open(destination_dir + '/' + srcfile[srcfile.rfind('/')+1:], 'a+') as f:
        f.write(gamelist)

    print('get_opening operation completed for file ' + srcfile)