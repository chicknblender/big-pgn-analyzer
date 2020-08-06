
def sanitize(pgn):
    # removes error-generating characters from a pgn before processing
    # should only have to be done once on source data

    # removes information inside of curly brackets from a string, e.g. engine analysis
    while "{" in pgn and "}" in pgn:
        start = pgn.find("{")
        end = pgn.find("}")
        if end > start:
            pgn = pgn[:start] + pgn[end+1:]
        else:
            pgn = pgn[end+1:]
    
    # remove redundant numbering (e.g. "1. e4 1... e5" becomes "1. e4 e5")
    while "..." in pgn:
        start = pgn.find("...") - 1
        while pgn[start-1:start] != " ":
            start -= 1
        end = pgn.find("...") + 3
        pgn = pgn[:start] + pgn[end:]
    
    # remove annotations such as !! and !?
    pgn = pgn.replace('?', '')
    pgn = pgn.replace('!', '')
    
    # add a space before the first move for easier searching
    pgn = pgn.replace('\n1. ', '\n 1. ')
    
    # remove redundant spaces
    while "  " in pgn: 
        pgn = pgn.replace("  ", " ")
        
    #remove redundant newlines
    while "\n\n\n" in pgn: 
        pgn = pgn.replace("\n\n\n", "\n\n")
        
    return(pgn)

def result(pgn):
    start = pgn.find("[Result \"") + len("[Result \"")
    if start == -1 + len("[Result \""):
        return False
    end = pgn.find("\"]", start)
    return pgn[start:end]

def get_move(pgn, parent_moves):
    pgn = strip_headers(pgn)
    pgn = pgn.replace('\n', ' ') # because we are searching for spaces, not newlines, to mark the end of a move
    
    start = pgn.find(parent_moves)
    if start == -1:
        return "PARENT NOT FOUND"
    start += len(parent_moves) + 1 # get to the end of the parent_moves substring
    end = pgn.find(" ", start + 2)
    move = pgn[start:end]
    if '*' in move or '1-0' in move or '0-1' in move or '1/2-1/2' in move:
        return "game over"
    if move[len(move)-1:] == ".": # then we've found a move number, not a move. Also, it's white's move.
        end = pgn.find(" ", end + 1) 
        move = pgn[start:end] # now contains number and move
        move = strip_spaces(move)
        return move
    
    # if we get here, it's black's move. we need to add the move number and '...'
    end = parent_moves.rfind('.')
    start = parent_moves[:end].rfind(' ') + 1
    move_number = parent_moves[start:end]
    move = str(move_number) + "... " + move
    move = strip_spaces(move)
    return move

def strip_headers(pgn):
    end_of_headers = pgn.rfind(']')
    if end_of_headers == -1:
        return pgn
    else:
        return pgn[end_of_headers + 1:]
            
def strip_spaces(movestr):
    while movestr[:1] == ' ':
        movestr = movestr[1:]
    while movestr[-1:] == ' ':
        movestr = movestr[:-1]
    return movestr
    
