
import pgnfx
import tree
import folder
import os
import pgndb
import prune
import transpositions


threshold = 5 # nodes with less than this percent of the total count will be pruned
# 0.01 is insane

def split(root):

    # prepare the root directory
    print('preparing root')
    pgndb.prepare_root(root)
    
    old_nodes = 0
    new_nodes = 1
    i = 1
    while new_nodes > old_nodes: # the last cycle generated new children somewhere so keep going
        print('iteration ' + str(i))
        i += 1
        old_nodes = tree.count_nodes(root)
        print(str(old_nodes) + ' nodes so far')
        
        print('splitting one level...')
        split_one_level(root)
        
        print('pruning the super-tiny nodes before transposition check...')
        prune.prune(root, (threshold / 100))
        
        print('fixing transpositions...')
        transpositions.find_and_merge(root, threshold)
        
        print('pruning below threshold...')
        prune.prune(root, threshold)
        
        print('updating node count...')
        new_nodes = tree.count_nodes(root)
        
    print(str(new_nodes) + ' nodes created.')

def split_one_level(root):
    if folder.istrans(root):
        return # don't split nodes that have been previously merged as transpositions
    if folder.issplit(root):
        # split the child nodes
        children = tree.children(root)
        if children == []: # this node is previously split, and all children were pruned 
            return
        for c in children:
            split_one_level(c)
    else: # we only get here if not already split
        split_children(root)
        
def split_children(root):
    
    # split children.pgn into new child directories
    parent_moves = folder.get_parent_moves(root)
    move_dict = {}
    with open(root + '/children.pgn', 'rt') as f:
        pgn = f.readline()
        for line in f:
            if not '[Event' in line:
                pgn += line
            else:
                # process this pgn
                move = pgnfx.get_move(pgn, parent_moves)
                if '*' in move:
                    pgn = line
                    continue
                move_dict = add_to_dict(pgn, move, move_dict, root)
                
                # reset for the next pgn
                pgn = line
                
    # process the last pgn
    move = pgnfx.get_move(pgn, parent_moves)
    move_dict = add_to_dict(pgn, move, move_dict, root)
    
    # write move_dict to flies
    dict_to_file(move_dict, root)
                    
    # make reports for all the new child directories
    folder.make_child_reports(root)
    
    # mark this folder as split
    with open(root + '/report.csv', 'a') as f:
        f.write('split,True\n')
        
    # delete this level's children.pgn
    # actually, let's not do that yet

def add_to_dict(pgn, move, move_dict, root):
    if ' bx' in move:
        move = move.replace(' bx', ' pbx')
    if move in move_dict:
        move_dict[move].append(pgn)
        if len(move_dict[move]) > 10000: 
            write_list_to_file(move, move_dict[move], root)
            move_dict[move] = []
    else:
        move_dict[move] = [pgn]
    return move_dict

def write_list_to_file(move, pgn_list, folder):
    if not (move in os.listdir(folder)):
        os.mkdir(folder + "/" + move)
    with open(folder + "/" + move + "/children.pgn", 'a+') as file:
        for pgn in pgn_list:
            file.write(pgn)
    
def dict_to_file(move_dict, root):
    for move in move_dict:
        write_list_to_file(move, move_dict[move], root)
