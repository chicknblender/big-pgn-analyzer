import os.path
import pgnfx
import chessfx
import enginefx
import tree

def issplit(folder):
    if os.path.exists(folder + '/report.csv'):
        with open(folder + '/report.csv', 'rt') as f:
            r = f.read()
        if 'split,True' in r:
            return True
        else:
            return False
    else:
        return False
    
def istrans(folder):
    with open(folder + '/report.csv', 'rt') as f:
        r = f.read()
    if 'transposition,True' in r:
        return True
    else:
        return False

def get_trans(folder):
    if not istrans(folder):
        return None
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    start = report.find('transposition,True,') + len('transposition,True,')
    end = report.find('\n', start)
    return report[start:end]

def get_parent_moves(folder):
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    start = report.find('parent moves,') + len('parent moves,')
    end = report.find('\n', start)
    return report[start:end]

def get_fen(folder):
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    start = report.find('fen,') + len('fen,')
    end = report.find('\n', start)
    return report[start:end]

def get_num_games(folder):
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    start = report.find('games,') + len('games,')
    end = report.find('\n', start)
    return int(report[start:end])

def get_percent(folder):
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    start = report.find('percent,') + len('percent,')
    end = report.find('\n', start)
    return float(report[start:end])

def get_ww(folder):
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    start = report.find('white wins,') + len('white wins,')
    end = report.find('\n', start)
    return int(report[start:end])

def get_bw(folder):
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    start = report.find('black wins,') + len('black wins,')
    end = report.find('\n', start)
    return int(report[start:end])

def get_eval(folder):
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()
    if not 'eval,' in report:
        return False
    start = report.find('eval,') + len('eval,')
    end = report.find('\n', start)
    return report[start:end]


def win_dif(folder): # white wins % - black wins %
    with open(folder + '/report.csv', 'rt') as f:
        report = f.read()

    start = report.find('games,') + len('games,')
    end = report.find('\n', start)
    n = int(report[start:end])
    
    start = report.find('white wins,') + len('white wins,')
    end = report.find('\n', start)
    ww = int(report[start:end])
    ww_percent = 100 * ww/n

    start = report.find('black wins,') + len('black wins,')
    end = report.find('\n', start)
    bw = int(report[start:end])
    bw_percent = 100 * bw/n
    
    return ww_percent - bw_percent
        
def same_move_number(d1, d2):
    d1 = d1[d1.rfind('/')+1:]
    d2 = d2[d2.rfind('/')+1:]
    d1 = d1[0:d1.find('.')]
    d2 = d2[0:d2.find('.')]
    return (d1 == d2)

def make_child_reports(root):
    dirlist = os.listdir(root)
    temp = []
    for item in dirlist:
        if os.path.isdir(root + '/' + item):
            temp.append(item)
    dirlist = temp
    for item in dirlist:
        make_report(item, root)
        
def make_report(d, root):
    move = d
    if '...' in move:
        move = move[move.find('... ') + 4:]
    parent_moves = pgnfx.strip_spaces(get_parent_moves(root) + ' ' + move)
    fen = chessfx.make_fen(parent_moves)
    with open(root + '/' + d + '/children.pgn', 'rt') as f:
        n = 0
        ww = 0
        bw = 0
        parent_n = get_num_games(root)
        parent_percent = get_percent(root)
        for line in f:
            if '[Event' in line:
                n += 1
            elif '[Result' in line and '1-0' in line:
                ww += 1
            elif '[Result' in line and '0-1' in line:
                bw += 1
    local_percent = 100 * n / parent_n
    percent = local_percent / 100 * parent_percent
        
    reportstr = 'parent moves,' + parent_moves + '\n' + \
                'fen,' + fen + '\n' + \
                'games,' + str(n) + '\n' + \
                'percent,' + str(percent) + '\n' + \
                'local percent,' + str(local_percent) + '\n' + \
                'white wins,' + str(ww) + '\n' + \
                'black wins,' + str(bw) + '\n'
        
    with open(root + '/' + d + '/report.csv', 'w') as f:
        f.write(reportstr)

def report_replace(reportstr, name, newval):
    start = reportstr.find(name)
    start = reportstr.find(',', start) + 1
    end = reportstr.find('\n', start)
    return reportstr[:start] + newval + reportstr[end:]

def add_eval(folder, sec):
    fen = get_fen(folder)
    x = enginefx.get_eval(fen, sec)
    evalstr = 'eval,'
    if x.is_mate():
        evalstr += 'mate,' + str(x.mate())
    else:
        evalstr += 'cp,' + str(x.cp) + '\n'
        
    with open(folder + '/report.csv', 'rt') as f:
        reportstr = f.read()
    while 'eval,' in reportstr: # remove the old eval
        start = reportstr.find('eval,')
        end = reportstr.find('\n', start)
        reportstr = reportstr[:start] + reportstr[end+1:]
        
    reportstr += evalstr
    with open(folder + '/report.csv', 'w') as f:
        f.write(reportstr)
        
def add_eval_all(root, sec):
    add_eval(root, sec)
    childs = tree.children(root)
    for c in childs:
        add_eval_all(c, sec)
    
