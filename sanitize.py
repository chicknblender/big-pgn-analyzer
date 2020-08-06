import pgndb
import pgnfx
import os
import os.path

def sanitize_dir(path):
    
    # produces a sanitized version of all .pgn files in a dir
    
    dirlist = os.listdir(path)
    temp = []
    for item in dirlist:
        if pgndb.ispgn(path + '/' + item):
            temp.append(path + '/' + item)
    dirlist = temp

    print(str(len(dirlist)) + ' PGN files found. Sanitizing all...')
    for item in dirlist:
        sanitize_db(item)
    print('sanitize_dir operation complete.')
    
def sanitize_db(path):
    
    if not pgndb.ispgn(path):
        print('sanitize_db given non-pgn path: ' + path)
        exit()
        
    newfile = path[:-4] + '-san.pgn'
    if os.path.isfile(newfile):
        x = input(newfile + ' already exists. Append to it? (y/n): ')
        if x != 'y':
            print('sanitize_db operation cancelled by user')
            exit()
                
    with open(path, 'rt') as f:
        pgn = f.readline()
        pgndb_str = ''
        games = 0
        for line in f:
            if not '[Event' in line:
                pgn += line
            else:
                # process this pgn
                games += 1
                pgn = pgnfx.sanitize(pgn)
                pgndb_str += pgn
                if games > 10000:
                    with open(newfile, 'a+') as nf:
                        nf.write(pgndb_str)
                    pgndb_str = ''
                    games = 0
                
                # reset for the next pgn
                pgn = line
                
    # process the last pgn
    pgn = pgnfx.sanitize(pgn)
    pgndb_str += pgn
    with open(newfile, 'a+') as nf:
        nf.write(pgndb_str)
    print(path + ' sanitized successfully. ' + newfile + ' created.')
