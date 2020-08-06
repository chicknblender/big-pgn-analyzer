# Generates a sanitized, "random" sample of PGN games from a PGN database

# verify these before executing!
source_file = 'e:/lichess_db_standard_rated_2020-05.pgn/lichess_db_standard_rated_2020-05.pgn'
result_file = 'e:/lichess_db_standard_rated_2020-05.pgn/sample2.pgn'
num = 8        # e.g. for num=2 and denom=20, pick 2 games at random from every 20 games 
denom = 60     # read sequentially from the source_file

import random
import pgnfx
import os
import os.path

def make():
    
    if os.path.exists(result_file):
        x = input(result_file + " already exists. Overwrite? (y / n): ")
        if x == 'y':
            os.remove(result_file)
        else:
            print("Execution halted.")
            exit()
            
    src_pgn_list = []
    res_pgn_list = []
    with open(source_file, 'rt') as f:
        pgn = f.readline()
        for line in f:
            if not '[Event' in line:
                pgn += line
            else:
                # process this pgn
                src_pgn_list.append(pgn)
                
                if len(src_pgn_list) == denom:
                    
                    # pick out the random games and put them in res_pgn_list
                    randlist = get_rand_list()
                    for n in randlist:
                        res_pgn_list.append(src_pgn_list[n])
                    
                    # dump the results to file if it's getting too big
                    if len(res_pgn_list) > 10000:
                        writefile(res_pgn_list)
                        res_pgn_list = []
                    
                    # clear out for the next round
                    src_pgn_list = []
                
                # restart for the next pgn
                pgn = line
                
    # write the remaining results
    writefile(res_pgn_list)
    

def get_rand_list():
    randlist = []
    for i in range(num):
        randnum = int(random.random() * denom)
        while randnum in randlist:
            randnum = int(random.random() * denom)
        randlist.append(randnum)
    return sorted(randlist)

def writefile(res_pgn_list):
    with open(result_file, 'a+') as f:
        for pgn in res_pgn_list:
            pgn = pgnfx.sanitize(pgn)
            f.write(pgn)
