# Goal:
#     Choose a side, white or black, to build repertoire from perspective of chosen side.
#     Choose a mode, auto or manual. Auto generates the whole repertoire at once, and manual prompts the user for move input at each stage.
#     Set a threshold at which to stop (based on move probability -- i.e. don't build a repertoire with moves that will never be played
#     Take a pgndb containing only games with the opening of interest.
#     
#     Start iterative process here:
#         Starting at a specified move number, split the pgndb into children and create reports for each new node.
#     
#         If it's the chosen side's move, DO NOT decrease the global percentage of the children
#             Use engine analysis and game outcome or elo change to rank the moves
#             Prepare a report with the analysis.
#             If running in manual mode:
#                 Display the analysis report.
#                 Prompt the user to chose one or more continuations.
#             If running in auto mode:
#                 Continue with the best move or moves (e.g. the best move and all moves within a certain score threshold below it).
#                 Move unchosen moves into their own directory
#                 
#         If it's the opponent's move:
#             Merge transpositions.
#             Prune nodes below the threshold.
    