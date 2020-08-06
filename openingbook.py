
o = [
    ('', "Opening Position"),
    ('1. e4', "King's Pawn"),
    ('1. d4', "Queen's Pawn"),
    ('1. e4 e5 2. Nf3 Nc6 3. Bc4', "Italian Game"),
    ('1. e4 e5 2. Nf3 Nc6 3. Bb5', "Ruy Lopez"),
    ('1. e4 e5 2. Nf3 Nc6 3. d4', 'Scotch Game'),
    ('1. e4 e5 2. Nf3 Nc6 3. Nc3', 'Three Knights'),
    ('1. e4 e5 2. Nf3 Nc6 3. Nc3 Nf6', 'Four Knights'),
    ('1. e4 e5 2. Nf3', 'King\'s Knight'),
    ('1. e4 e5', "Open Game"),
    ('1. e4 e5 2. Nf3 Nc6 3. Bc4 Nf6', 'Two Knights Defense'),
    ('1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5', 'Giuoco Piano'),
    ('1. e4 e5 2. Nf3 Nc6 3. Bc4 h6', 'Anti-Fried Liver'),
    ('1. e4 e5 2. Nf3 Nc6 3. Bb5 d6', 'Steinitz Defense'),
    ('1. e4 e5 2. Nf3 d6', 'Philidor Defense'),
    ('1. e4 e5 2. Nf3 Nf6', "Petrov's Defense"),
    ('1. e4 e5 2. Nf3 Qf6', 'McConnell Defense'),
    ('1. e4 e5 2. Bc4', 'Bishop\'s Opening'),
    ('1. e4 e5 2. f4', "King's Gambit"),
    ('1. e4 d5', 'Scandinavian Defense'),
    ('1. e4 c5', 'Sicilian Defense'),
    ('1. e3', "Van't Kruijs"),
    ('1. c4', "English"),
    ('1. Nf3', 'Réti'),
    ('1. g3', 'Hungarian'),
    ('1. f4', 'Bird'),
    ('1. b3', 'Nimzowitsch-Larsen'),
    ('1. d3', 'Mieses'),
    ('1. b4', 'Orangutan'),
    ('1. e4 e6', 'French Defense'),
    ('1. e4 c6', 'Caro-Kann Defense'),
    ('1. e4 d6', 'Pirc Defense'),
    ('1. e4 g6', 'Modern Defense'),
    ('1. e4 b6', 'Owen Defense'),
    ('1. e4 e5 2. d4', 'Center Game'),
    ('1. d4 d5 2. c4', "Queen's Gambit"),
    ('1. d4 d5 2. e4', 'Blackmar Gambit'),
    ('1. e4 Nf6', 'Alekhine Defense'),
    ('1. e4 Nc6', 'Nimzowitsch Defense'),
    ('1. e4 e5 2. Qh5', 'Danvers'),
    ('1. e4 c5 2. Nf3 Nc6', 'Old Sicilian'),
    ('1. e4 c5 2. Nf3 e6', 'Sicilian: French Var.'),
    ('1. d4 d5 2. c4 dxc4', "QG Accepted"),
    ('1. d4 d5 2. c4 e6', "QG Declined"),
    ('1. e4 e5 2. f4 exf4', "KG Accepted"),
    ('1. d4 d5 2. Nf3', 'Zukertort Var.'),
    ('1. d4 d5', "Closed Game"),
    ('1. d4 e6', "Horwitz Defense"),
    ('1. d4 Nf6', 'Indian Game'),
    ('1. e4 e6 2. Nf3', "French: Knight Var."),
    ('1. e4 c5 2. Bc4', 'Bowdler Attack'),
    ('1. d4 g6', 'Modern Defense'),
    ('1. d4 e5', 'Englund Gambit'),
    ('1. d4 c5', 'Old Benoni Defense'),
    ('1. e4 e5 2. Nc3', 'Vienna Game'),
    ('1. e4 c5 2. Nc3', 'Closed Sicilian'),
    ('1. e4 c5 2. Nf3 Nc6 3. d4', 'Open Sicilian'),
    ('1. d4 d5 2. c4 c6', 'Slav Defense'),
    ('1. e4 d5 2. d4', 'Blackmar Gambit'),
    ('1. e4 d5 2. e5 e6 3. d4', 'French Defense: Advance Var.'),
    ('1. e4 d5 2. e5 Nc6 3. d4', 'Nimzowitsch Defense: Scandinavian Var.'),
    ('1. e4 d5 2. exd5 c6', 'Blackburne-Kloosterboer Gambit'),
    ('1. e4 d5 2. exd5 Nf6', 'Modern Var.'),
    ('1. e4 d5 2. exd5 Nf6 3. d4 Nxd5', 'Marshall Var.'),
    ('1. e4 d5 2. exd5 Qxd5', 'Mieses-Kotroc Var.'),
    ('1. e4 d5 2. exd5 Qxd5 3. Nc3 Qa5', 'Scandinavian: Main Line'),
    ('1. e4 d5 2. exd5 Qxd5 3. Nc3 Qa5 4. d4 Nf6', 'Main Line: Mieses Var.'),
    ('1. e4 d5 2. exd5 Qxd5 3. Nc3 Qd6', ' Gubinsky-Melts Defense'),
    ('1. e4 d5 2. Nf3', 'Zukertort: Tennison Gambit'),
    ('1. e4 d5 2. exd5 Nf6 3. c4 e6', 'Icelandic Gambit'),
    ('1. e4 d5 2. exd5 Nf6 3. d4 Bg4', 'Portuguese Var')    
    ]

def add_names(node_list):

    for node in node_list:
        p = node['parent moves']
        for name in o:
            if name[0] == node['parent moves']:
                node['label'] = node['label'] + ' (' + name[1] + ')'
    
    return node_list