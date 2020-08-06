import shutil
import tree
import folder

def prune(root, threshold):
    
    # delete this node if it's a faggot node
    if 'PARENT NOT FOUND' in root or 'game over' in root:
        shutil.rmtree(root)

    # delete this node if it is below threshold
    elif folder.get_percent(root) < threshold:
        shutil.rmtree(root)
    else:
        # prune child nodes
        children = tree.children(root)
        for c in children:
            prune(c, threshold)
            
def prune_bottom(root):
    # just deletes the lowest existing level of the tree, except will not delete the root itself
    depth = tree.depth(root)
    if depth == 1:
        print('prune_bottom error: no children at root level')
    else:
        children = tree.children(root)
        for c in children:
            prune_bottom_h(c, depth - 1)
            
def prune_bottom_h(root, depth):
    if depth == 1:
        shutil.rmtree(root)
    else:
        children = tree.children(root)
        for c in children:
            prune_bottom_h(c, depth - 1)