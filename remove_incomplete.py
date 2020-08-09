import pgndb
import pgnfx
import os
import os.path
import time


def remove_incomplete_dir(path):
    # produces a sanitized version of all .pgn files in a dir

    dirlist = os.listdir(path)
    temp = []
    for item in dirlist:
        if pgndb.ispgn(path + '/' + item):
            temp.append(path + '/' + item)
    dirlist = temp

    print(str(len(dirlist)) + ' PGN files found. Removing incomplete from all...')
    for item in dirlist:
        remove_imcomplete_db(item)
    print('remove_incomplete_dir operation complete.')


def remove_imcomplete_db(path):
    if not pgndb.ispgn(path):
        print('remove_incomplete1_db given non-pgn path: ' + path)
        exit()

    newfile = path[:-4] + '-ri.pgn'
    if os.path.isfile(newfile):
        x = input(newfile + ' already exists. Append to it? (y/n): ')
        if x != 'y':
            print('remove_incomplete_db operation cancelled by user')
            exit()

    start = time.time()
    with open(path, 'rt') as f:
        pgn = f.readline()
        pgndb_str = ''
        games = 0
        for line in f:
            if not '[Event' in line:
                pgn += line
            else:
                # process this pgn
                res = pgnfx.result(pgn)
                if (res == '1-0') or (res == '0-1') or res == ('1/2-1/2'):
                    games += 1
                    pgndb_str += pgn
                    if games > 100000:
                        with open(newfile, 'a+') as nf:
                            nf.write(pgndb_str)
                        pgndb_str = ''
                        games = 0

                # reset for the next pgn
                pgn = line

    # process the last pgn
    res = pgnfx.result(pgn)
    if (res == '1-0') or (res == '0-1') or res == ('1/2-1/2'):
        pgndb_str += pgn

    # write the remaining pgns to file
    with open(newfile, 'a+') as nf:
        nf.write(pgndb_str)

    end = time.time()
    print(path + ' remove_incomplete successful. ' + newfile + ' created.')
    sec = end - start
    print('Operation complete in {0} seconds'.format(sec))
