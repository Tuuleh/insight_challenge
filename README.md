insight_challenge
=================

By: Tuuli Pöllänen<br>
Date: 31.10.2014

<h2>Task and instructions</h2>
This repository contains my contribution to the Sudoku-puzzle coding challenge for the Insight Data Engineering Fellowship. The description of the challenge is as follows:<br>

We'd like you to implement a Sudoku puzzle solver in one of the following programming languages: Java, Clojure, Scala, C, C++, Python, or Ruby. It should input a CSV file consisting of an unsolved Sudoku with 0's representing blanks, and output a CSV file with the solved Sudoku. <br>

For instance, the input CSV file can look like the following:<br>
0,3,5,2,9,0,8,6,4<br>
0,8,2,4,1,0,7,0,3<br>
7,6,4,3,8,0,0,9,0<br>
2,1,8,7,3,9,0,4,0<br>
0,0,0,8,0,4,2,3,0<br>
0,4,3,0,5,2,9,7,0<br>
4,0,6,5,7,1,0,0,9<br>
3,5,9,0,2,8,4,1,7<br>
8,0,0,9,0,0,5,2,6<br>

The output should be:<br>

1,3,5,2,9,7,8,6,4<br>
9,8,2,4,1,6,7,5,3<br>
7,6,4,3,8,5,1,9,2<br>
2,1,8,7,3,9,6,4,5<br>
5,9,7,8,6,4,2,3,1<br>
6,4,3,1,5,2,9,7,8<br>
4,2,6,5,7,1,3,8,9<br>
3,5,9,6,2,8,4,1,7<br>
8,7,1,9,4,3,5,2,6<br>

Any additional game play features are optional, but welcome.

<h2>The solution</h2>

This Python-based program prompts the user for a text file containing a sudoku puzzle in csv-format, solves the puzzle, and outputs the solution in another .csv file. 

In the task, I refer to the entire 81-square 'play area' as the <i>grid</i>. The vertical elements are <i>rows</i>, the column elements are <i>columns</i>, and the nine 3x3 units in the grid are <i>boxes</i>. Each square belongs to three <i>units</i>: a row, a column and a box. Each square has twenty <i>peers</i>, or other squares that belong to the same units. Peers to a square cannot contain the same value as that square. Following this "naming convention", the variable names in the code should quite intuitive. 

Each square has its own "identification code", with an alphabetical character from A to I indicating its row, and a digit between 1 and 9 indicating its row. (e.g. the units for the first row are A1, A2, A3... A9, and the last column A9, B9, C9, ..., I9. The units and peers of each square are contained in dictionaries, with the square's identification code as key and lists of the squares' units (or peers) as values. At the start of the program, it computes a dictionary containing all the possible values for each square, and the possible values of this dictionary are gradually eliminated to arrive at the solution.

The program uses a combination of two heuristic strategies, the 'naked twins'-strategy, and recursive search to solve the puzzle. The heuristic strategies are the following:

<i> a) If there is only one possible value for the square, that value cannot be contained by its peers (squares in the same row, column or box). Therefore, that value can be eliminated from its peers.<br>
<i> b) If a unit (row, column or box) has only one possible place for a value, the value must be placed in that location.

A failure in either heuristic strategy implies a contradiction in the puzzle. For simpler puzzles, the heuristic strategies are often enough to arrive at a solution, whereas more difficult ones rely on recursive search.

The naked twins strategy is used when two squares are found within the same unit, containing only the same two digits. This means that no other square in the same unit can contain either of the values, and so the values can safely be removed from all the other squares in the unit.

<h2>Running the program</h2>
This is a simple command line program that has been tested with Python 2.7. To run it, clone the repository, go into the folder that is created, and run the program by typing 'sudoku.py'. When prompted, type in the name of the file that contains your puzzle (it has to be a .csv or a .txt file) - the results get stored into a new .csv file with _solution appended to your original filename - e.g. from "sudoku.csv" to "sudoku_solution.csv". 
