# big-pgn-analyzer
Process extremely large chess PGN files

Beware, this project is very rough at the moment! 

Working, sort of:

* Split arbitrarily large PGN files into smaller files based on moves played, player rating, time control, etc. 
* Create a nested directory structure containinging the sub-PGNs, with the directory structure representing the tree of moves played.
* Find and merge transposing positions.
* Create Sankey flow diagrams of chess openings.

Known issues:

* The Sankey diagrams don't handle tranpositions well.
* The code is generally finicky.

Goals:

* Cleanup ugly and/or inefficient code.
* Improve workflow/usability.
* Add engine analysis to positions.
* Integrate engine analysis with data from the PGN such as win probability to generate opening repertoires. 

Current Workflow:

* (Currently optional) Use sanitize.py to "clean" a large PGN database (removes annotations, commentary, engine analysis, etc to greatly reduce filesize and make processing easier.
* If a randomish sample from a large PGN db is desired, creat the sample with sample.py
* If one opening in particular is of interest, create a PGN of games with only that opening using get_opening.py.
* Use split.py to iteratively split a PGN out by opening moves. 
* If needed to free up storage space, remove the sub-PGNs with del_pgns.py
* Creat charts with sankey.py
