import os
import os.path

def del_pgns(root):
    x = input("Really delete all subdir PGNs in directory " + root + "? (y/n)")
    if x != 'y':
        print('Operation cancelled.')
        return
    else:
        paths = os.listdir(root)
        for p in paths:
            if os.path.isdir(root + '/' + p):
                del_pgns_h(root + '/' + p)
        print('Operation completed.')
        
def del_pgns_h(root):
    paths = os.listdir(root)
    for p in paths:
        if os.path.isdir(root + '/' + p):
            del_pgns_h(root + '/' + p)
        elif '.pgn' in p:
            os.remove(root + '/' + p)