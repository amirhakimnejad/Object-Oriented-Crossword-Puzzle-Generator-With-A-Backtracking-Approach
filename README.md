# About the problem
The examples and the core structure of the problem is inspired from a project defined at Harvard's CS50’s course [Introduction to Artificial Intelligence with Python](https://cs50.harvard.edu/ai/2020/) by 
Brian Yu
brian@cs.harvard.edu and 
David J. Malan
malan@harvard.edu.

Please take a look at the project and the idea of it here at the [project's page](https://cs50.harvard.edu/ai/2020/projects/3/crossword/).

# About the solution
Steps of the program
1. Read the words file and create a list of the words. (we removed illegal words here to prevent further exceptions)
2. Read a defined pattern in the patterns folder and create a python list of the pattern.
3. Feed the pattern and the words list to the Crossword class
4. The class constructor uses them to create a validated crossword pattern, with its list of required words(horizontal and vertical), 
5. It creates a list of answers for it(with shuffled words - it means you can run it multiple times and keep/compare different answers and pick the best one) using a brute force algorithm.
6. Now the class contains everything you need to solve, debug, and validate the puzzle.


## The brute force algorithm steps
1. Validate the pattern and the words list.
2. Make a shuffled, then sorted list of required words
3. Create a copy list of the all words list and call it available words list.
4. Create a list of required words for the pattern.
5. If the list of required words is not empty, pop the biggest required word from the list of required words to try and find an answer for it.
    - Otherwise, the puzzle is solved.
    
6. Find all available words that can be used to fill the required word.(We call them available words, because they're not repeated, they match the length, and all other already picked answers match with them if they intersect with it in our 2D pattern)
    - Sort them by any relation you can find between them and the already picked answers.
    - If any word found , pick one as an answer and push it to the answers stack, remove the word from available words, and go to step 5
    - Otherwise, If the answers stack is empty, the puzzle is failed.
        - If answers stack is not empty, pop the last answer from the answers stack, insert it as a required word at the end of required words list again, bring back all the smaller words from the all words list and add them to the available words again, and go to step 5


## Example input, output
Code to run the program:
``` bash
python3 cross_word_puzzle_generator.py
```

Program that runs
``` python
def main():
    crossword_puzzle = create_a_level()
    crossword_puzzle.get_pattern().draw()
    CrossWordWord.print_words_info(crossword_puzzle.get_pattern().get_mock_words())
    CrossWordWord.print_words_info(crossword_puzzle.get_answers())

if __name__ == "__main__":
    main()
```

Output

``` text
Pattern:
['_', '_', '_', '_', '_', '#']
['_', '#', '#', '_', '#', '#']
['_', '#', '#', '_', '#', '_']
['#', '_', '#', '_', '_', '_']
['#', '_', '#', '#', '#', '_']
['#', '_', '_', '_', '_', '_']
------------------------------
Word: ['_', '_', '_', '_', '_']
_ at 0, 0
_ at 0, 1
_ at 0, 2
_ at 0, 3
_ at 0, 4
Starting x: 0
Starting y: 0
Direction: Horizontal
Length: 5
Filled: False
------------------------------
------------------------------
Word: ['_', '_', '_']
_ at 3, 3
_ at 3, 4
_ at 3, 5
Starting x: 3
Starting y: 3
Direction: Horizontal
Length: 3
Filled: False
------------------------------
------------------------------
Word: ['_', '_', '_', '_', '_']
_ at 5, 1
_ at 5, 2
_ at 5, 3
_ at 5, 4
_ at 5, 5
Starting x: 5
Starting y: 1
Direction: Horizontal
Length: 5
Filled: False
------------------------------
------------------------------
Word: ['_', '_', '_']
_ at 0, 0
_ at 1, 0
_ at 2, 0
Starting x: 0
Starting y: 0
Direction: Vertical
Length: 3
Filled: False
------------------------------
------------------------------
Word: ['_', '_', '_']
_ at 3, 1
_ at 4, 1
_ at 5, 1
Starting x: 3
Starting y: 1
Direction: Vertical
Length: 3
Filled: False
------------------------------
------------------------------
Word: ['_', '_', '_', '_']
_ at 0, 3
_ at 1, 3
_ at 2, 3
_ at 3, 3
Starting x: 0
Starting y: 3
Direction: Vertical
Length: 4
Filled: False
------------------------------
------------------------------
Word: ['_', '_', '_', '_']
_ at 2, 5
_ at 3, 5
_ at 4, 5
_ at 5, 5
Starting x: 2
Starting y: 5
Direction: Vertical
Length: 4
Filled: False
------------------------------
------------------------------
Word: ['S', 'H', 'E', 'L', 'L']
S at 5, 1
H at 5, 2
E at 5, 3
L at 5, 4
L at 5, 5
Starting x: 5
Starting y: 1
Direction: Horizontal
Length: 5
Filled: True
------------------------------
------------------------------
Word: ['S', 'H', 'E', 'L', 'F']
S at 0, 0
H at 0, 1
E at 0, 2
L at 0, 3
F at 0, 4
Starting x: 0
Starting y: 0
Direction: Horizontal
Length: 5
Filled: True
------------------------------
------------------------------
Word: ['H', 'E', 'L', 'L']
H at 2, 5
E at 3, 5
L at 4, 5
L at 5, 5
Starting x: 2
Starting y: 5
Direction: Vertical
Length: 4
Filled: True
------------------------------
------------------------------
Word: ['L', 'O', 'S', 'E']
L at 0, 3
O at 1, 3
S at 2, 3
E at 3, 3
Starting x: 0
Starting y: 3
Direction: Vertical
Length: 4
Filled: True
------------------------------
------------------------------
Word: ['Y', 'E', 'S']
Y at 3, 1
E at 4, 1
S at 5, 1
Starting x: 3
Starting y: 1
Direction: Vertical
Length: 3
Filled: True
------------------------------
------------------------------
Word: ['S', 'E', 'E']
S at 0, 0
E at 1, 0
E at 2, 0
Starting x: 0
Starting y: 0
Direction: Vertical
Length: 3
Filled: True
------------------------------
------------------------------
Word: ['E', 'Y', 'E']
E at 3, 3
Y at 3, 4
E at 3, 5
Starting x: 3
Starting y: 3
Direction: Horizontal
Length: 3
Filled: True
------------------------------
```



## Some things that maybe useful to add
- Maybe limit looping to a certain number of iterations? :white_check_mark:
- Maybe add a way to stop the algorithm if it's taking too long? :white_check_mark:
- Adding more test cases :white_check_mark:
- Maybe easily support non-square grids? :x:
- Looping for a certain time, find possible puzzles for a pattern and then rate them and pick the best ones :white_check_mark:
- Sort picked ones by the most intersections :white_check_mark:
- Sort with most intersections


## *Any issues, comments and pull requests are welcome.*


# Licence
This project is licensed under the MIT License.

