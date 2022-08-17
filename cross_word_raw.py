pattern = "#    \n  ###\n   # \n # # \n##   "
MinimumAcceptedLength = 2
MaximumAcceptedLength = 10
words = ['cat', 'dog', 'mouse', 'horse', 'cow', 'pig', 'sheep',
         'chicken', 'duck', 'goose', 'fish', 'bird', 'snake',
         'lizard', 'turtle', 'ant', 'bee', 'beetle', 'butterfly',
         'caterpillar', 'cockroach', 'crocodile', 'dinosaur', 'elephant',
         'fish', 'frog', 'giraffe', 'hedgehog', 'kangaroo', 'lion',
         'monkey', 'octopus', 'owl', 'penguin', 'rabbit', 'rat',
         'snail', 'snake', 'spider', 'tiger', 'whale', 'zebra']
accepted_characters_in_pattern = ['#', ' ']


class CrosswordPattern():
    cols = []
    rows = []
    size = 0

    def __init__(self, pattern_string):
        self.rows = pattern_string.split('\n')
        self.rows = [[char for char in row] for row in self.rows]
        self.size = len(self.rows)
        if self.size < MinimumAcceptedLength:
            raise Exception(
                'Crossword pattern must have at least %s rows.', MinimumAcceptedLength)
        if self.size > MaximumAcceptedLength:
            raise Exception(
                'Crossword pattern must have at most %s rows.', MaximumAcceptedLength)
        self.cols = [[] for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                self.cols[j].append(self.rows[i][j])

        for row in self.rows:
            if len(self.rows) != self.size:
                raise Exception(
                    'Invalid crossword pattern, each row must have the same length')
            for char in row:
                if char not in accepted_characters_in_pattern:
                    raise Exception(
                        'Invalid crossword pattern, only \'#\' and \' \' are allowed - %s' % char)

        if len(self.cols) != self.size:
            raise Exception(
                'Invalid crossword pattern, each column must have the same length')
    
    def draw(self, direction='horizontal'):
        matrix_to_draw = [[]]
        if direction == 'horizontal':
            matrix_to_draw = self.rows
        else:
            matrix_to_draw = self.cols
        for row in matrix_to_draw:
            print(row)

class CrossWordLetter():
    __character = ''
    x = -1
    y = -1

    @classmethod
    def is_valid_character(character):
        return character.isalpha() or character in accepted_characters_in_pattern

    def __init__(self, character='', x=-1, y=-1):
        if character and CrossWordLetter.is_valid_character(character):
            raise Exception('Invalid character')

        self.__character = character
        self.x = x
        self.y = y

    def is_filled(self):
        return self.__character != ' '
    
    def is_found(self):
        return is_alpha(self.__character)
    
    def is_block(self):
        return self.__character == '#'
    
    def get_character(self):
        return self.__character


class CrossWordWord():
    __starting_x = -1
    __starting_y = -1
    __direction = "Horizontal"
    __letters = []
    __length = 0

    def is_filled(self):
        for letter in self.__letters:
            if not letter.is_filled():
                return False
        return True

    def fill_word(self, word_string):
        if self.direction == "Horizontal" and ((self.starting_x + len(word_string)) > self.__length):
            raise Exception("Invalid horizontal word")
        if self.direction == "Vertical" and ((self.starting_y + len(word_string)) > self.__length):
            raise Exception("Invalid vertical word")

        self.__letters = []
        for letter, i in word_string, range(len(word_string)):
            if self.__direction == "Horizontal":
                self.__letters.append(CrossWordLetter(
                    letter, self.__starting_x + i, self.__starting_y))
            else:
                self.__letters.append(CrossWordLetter(
                    letter, self.__starting_x, self.__starting_y + i))

        if '#' in self.__letters:
            raise Exception("Invalid placement of word")

        if not isinstance(self.__letters, CrossWordLetter(list)):
            raise TypeError("letters must be set to a list")

    def __init__(self, starting_x, starting_y, direction, length, word_string=None):
        if length < MinimumAcceptedLength or length > MaximumAcceptedLength:
            raise Exception("Invalid word length")
        self.__length = length

        if not isinstance(starting_x, int):
            raise TypeError("x must be set to an integer")
        if starting_x < 0 or starting_x > len(crossword_pattern.cols):
            raise ValueError("x must be between 0 and %s" % len(pattern.cols))
        self.__starting_x = starting_x

        if not isinstance(starting_y, int):
            raise TypeError("y must be set to an integer")
        if starting_y < 0 or starting_y > len(crossword_pattern.rows):
            raise ValueError("y must be between 0 and %s" % len(pattern.rows))
        self.__starting_y = starting_y

        if not isinstance(direction, str):
            raise TypeError("direction must be set to a string")
        if direction not in ["Horizontal", "Vertical"]:
            raise ValueError(
                "direction must be either 'Horizontal' or 'Vertical'")
        self.__direction = direction

        if word_string:
            self.fill_word(word_string)


class Crossword():
    __all_letters = []
    __all_word_placements = []
    __pattern = None
    __answers = []
    __length = 0

    def __init__(self, pattern):
        self.__pattern = CrosswordPattern(pattern)
        self.__length = self.__pattern.size
        self.__all_letters = [[CrossWordLetter() for i in range(self.__pattern.size)] for i in range(self.__pattern.size)]
        self.__answers = self.extract_all_possible_word_places()

    def extract_all_possible_word_places(self):
        pass
    
    def print_crossword(self):
        for i in range(self.__length):
            for j in range(self.__length):
                print(self.__all_letters[i][j].get_character(), end="")
            print(",")
    def get_pattern(self):
        return self.__pattern


def main():
    crossword = Crossword(pattern)
    crossword.get_pattern().draw()
    crossword.print_crossword()


if __name__ == "__main__":
    main()