import tree
import folder
import openingbook

def get_nodes(root, threshold):
    
    if folder.istrans(root):
        trans = folder.get_trans(root)
    else:
        trans = ''
        
    this_node = {
        'label' : folder.get_parent_moves(root),
        'source' : 0,
        'target' : 0,
        'value' : 0,
        'win_dif' : folder.win_dif(root),
        'path' : root,
        'parent moves' : folder.get_parent_moves(root),
        'transposition' : trans
        }
    
    node_list = [this_node]
    children = tree.children(root)
    for c in children:
        node_list = get_nodes_h(c, node_list, this_node, threshold)
    node_list = add_xy(node_list, root)
    node_list = link_transpositions(node_list)
    node_list = openingbook.add_names(node_list)
    node_report(node_list, root)
    return node_list
    
def get_nodes_h(path, node_list, parent, threshold):
    if folder.get_percent(path) < threshold:
        return node_list

    if folder.istrans(path):
        trans = folder.get_trans(path)
    else:
        trans = ''

    this_node = {
        'label' : path[path.rfind('/')+1:],
        'source' : parent['target'],
        'target' : len(node_list),
        'value' : folder.get_percent(path),
        'win_dif' : folder.win_dif(path),
        'path' : path,
        'parentpath' : parent['path'],
        'parentvalue' : parent['value'],
        'parent moves' : folder.get_parent_moves(path),
        'transposition' : trans
        }
    
    node_list.append(this_node)
    children = tree.children(path)
    if children == []:
        return node_list
    else:
        for c in children:
            node_list = get_nodes_h(c, node_list, this_node, threshold)
        return node_list

def add_xy(node_list, root):
    node_list = add_x(node_list, root)
    node_list = add_y(node_list)
    return node_list
    
def add_x(node_list, root):
    # determine depth of tree
    root_depth = root.count('/')
    leaf_depth = 0
    for node in node_list:
        if node['path'].count('/') > leaf_depth:
            leaf_depth = node['path'].count('/')

    # divide nodes evenly between 0 and 1, with padding on either side
    lpadding = 0
    rpadding = 0.1
    inc = (1 - (lpadding + rpadding)) / (leaf_depth - root_depth)
    for node in node_list:
        this_depth = node['path'].count('/') + 1 - root_depth
        node['x'] = lpadding + (inc * (this_depth - 1))
    return node_list
    
def add_y(node_list):
    # determine tree depth
    root_depth = node_list[0]['path'].count('/')
    leaf_depth = 0
    for node in node_list:
        if node['path'].count('/') > leaf_depth:
            leaf_depth = node['path'].count('/')
    depth = leaf_depth - root_depth + 1
        

    blend = 0.5 # 0 = space equally, 1 = space entirely based on value
    parabolize = 0.3 # 0 = top straight across; 0.5 means second column compressed by 50%
    reduction_factor = 0.6 # multiplied by parabolize with each iteration
    
    # for each depth level:
    for d in range(1, depth+1):
        
        # make list of nodes at this depth 
        node_loc = []
        i = 0
        for node in node_list:
            if node['path'].count('/') + 1 - root_depth == d:
                node_loc.append(i)
            i += 1

        n = len(node_loc)
        
        if n == 1: # slap that sucker down
            node_list[node_loc[0]]['y'] = 0

        else:
            # sort first by parent y-value, then by flow

            node_loc = y_sort(node_loc, node_list)
            equal_space = (1 - parabolize) / (n - 1)
            
            total_val = 0
            for loc in node_loc:
                total_val += node_list[loc]['value']
            total_val = total_val 
                
            i = 0
            pos = parabolize
            for loc in node_loc:
                node_list[loc]['y'] = pos
                pos += (node_list[loc]['value'] * (1 - parabolize) / total_val * blend) + \
                       (equal_space * (1 - blend))
                i += 1
            
            parabolize = parabolize * reduction_factor
        
    return node_list

def y_sort(node_loc, node_list):
    # sorts first by parent node y - working
    for i in node_loc:
        node_list[i]['parent_y'] = parent_y(i, node_list)
    node_loc = sorted(node_loc, key = lambda i : (node_list[i]['parent_y'], -node_list[i]['value']))

    return node_loc
        
        
def parent_y(i, node_list):
    parent_node_loc = node_list[i]['source']
    parent_node = node_list[parent_node_loc]
    return parent_node['y']

def node_report(node_list, root):
    report = 'label,moves,fen,games,percent,white wins,black wins,win difference,transposition\n'
    for n in node_list:
        report += n['label'] + ',' + \
                  n['parent moves'] + ',' + \
                  folder.get_fen(n['path']) + ',' + \
                  str(folder.get_num_games(n['path'])) + ',' + \
                  str(folder.get_percent(n['path'])) + ',' + \
                  str(folder.get_ww(n['path'])) + ',' + \
                  str(folder.get_bw(n['path'])) + ',' + \
                  str(n['win_dif']) + ',' + \
                  n['transposition'] + '\n'
    with open(root + '/node_report.csv', 'w') as f:
        f.write(report)
        
def link_transpositions(nl):
    for i in range(len(nl)):
        trans = nl[i]['transposition']
        if trans != '':
            print('moves ' + nl[i]['parent moves'])
            print('trans = ' + trans + ' | index = ' + str(i))
            transmoves = folder.get_parent_moves('../' + trans)
            print('transmoves = ' + transmoves)
            for j in range(len(nl)):
                moves = nl[j]['parent moves']
                if transmoves == moves:
                    print('par = ' + moves + ' | index = ' + str(j))
                    nl[i]['target'] = j
                    break
    return nl
                
    