pattern = "#    \n  ###\n   # \n # # \n##   "
MinimumAcceptedLength = 3
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

        self.check_if_pattern_is_valid()

    # TODO: check if all possible words are legal.
    def check_if_pattern_is_valid(self):
        pass

    def draw(self, direction='Horizontal'):
        matrix_to_draw = [[]]
        if direction == 'Horizontal':
            matrix_to_draw = self.rows
        elif direction == 'Vertical':
            matrix_to_draw = self.cols
        else:
            raise Exception('Invalid direction')
        for row in matrix_to_draw:
            print(row)


class CrossWordLetter():
    __character = ''
    x = -1
    y = -1

    @staticmethod
    def is_valid_character(character):
        return character.isalpha() or character in accepted_characters_in_pattern

    def __init__(self, character, x, y):
        if not CrossWordLetter.is_valid_character(character):
            raise Exception('Invalid character %s' % character)

        self.__character = character
        self.x = x
        self.y = y

    def is_filled(self):
        return self.__character != ' ' and self.__character != ''

    def is_found(self):
        return is_alpha(self.__character)

    def is_block(self):
        return self.__character == '#'

    def get_character(self):
        return self.__character


class CrossWordWord():
    __starting_x = -1
    __starting_y = -1
    __direction = ""
    __letters = []
    __length = -1

    def __init__(self, starting_x, starting_y, direction, length, word_string=None):
        if length < MinimumAcceptedLength or length > MaximumAcceptedLength:
            raise Exception("Invalid word length")
        self.__length = length

        if not isinstance(direction, str):
            raise TypeError("direction must be set to a string")
        if direction not in ["Horizontal", "Vertical"]:
            raise ValueError(
                "direction must be either 'Horizontal' or 'Vertical'")

        if direction == "Horizontal" and (abs(starting_x - length) > self.__length):
            raise Exception("Invalid horizontal word %s %s %s %s" % (
                starting_x, length, self.__length, word_string))
        if direction == "Vertical" and (abs(starting_y - length) > self.__length):
            raise Exception("Invalid vertical word")

        self.__direction = direction

        if not isinstance(starting_x, int):
            raise TypeError("x must be set to an integer")
        if starting_x < 0:
            raise ValueError("x must be between 0 and %s but is %s" %
                             (self.__length, starting_x))
        self.__starting_x = starting_x

        if not isinstance(starting_y, int):
            raise TypeError("y must be set to an integer")
        if starting_y < 0:
            raise ValueError("y must be between 0 and %s but is %s" %
                             (self.__length, starting_y))

        self.__starting_y = starting_y
        if word_string is None:
            word_string = " " * self.__length
        self.fill_word(word_string)

    def is_filled(self):
        for letter in self.__letters:
            if not letter.is_filled():
                return False
        return True

    def fill_word(self, word_string):
        self.__letters = []
        for letter, i in zip(word_string, range(len(word_string))):
            if self.__direction == "Horizontal":
                self.__letters.append(CrossWordLetter(
                    letter, self.__starting_x + i, self.__starting_y))
            elif self.__direction == "Vertical":
                self.__letters.append(CrossWordLetter(
                    letter, self.__starting_x, self.__starting_y + i))
            else:
                raise Exception("Invalid direction")

        if '#' in self.__letters:
            raise Exception("Invalid placement of word")

        if not isinstance(self.__letters, type([CrossWordLetter])):
            raise TypeError("letters must be set to a list")

        if len(word_string) != len(self.__letters):
            raise Exception("Invalid word length")

    def print_info(self):
        print("Word: %s" % [letter.get_character()
              for letter in self.__letters])
        print("Starting x: %s" % self.__starting_x)
        print("Starting y: %s" % self.__starting_y)
        print("Direction: %s" % self.__direction)
        print("Length: %s" % self.__length)
        print("Filled: %s" % self.is_filled())


class Crossword():
    __all_word_placements = []
    __pattern = None
    __answers = []
    __length = -1

    def __init__(self, pattern):
        self.__pattern = CrosswordPattern(pattern)
        self.__length = self.__pattern.size
        self.__fill_all_possible_word_places()

    def try_make_word_placement_from_string(self, word_string, starting_position, direction):
        try:
            word = CrossWordWord(
                starting_x=starting_position[0], starting_y=starting_position[1], direction=direction, length=len(word_string))
            return word
        except Exception as e:
            return None

    def ــfind_word_placements_of_2d_letters(self, two_dimensional_pattern, size, direction):
        exported_word_placements = []
        for row, i in zip(two_dimensional_pattern, range(size)):
            current_word = ""
            word_to_add = None
            starting_position = (-1, -1)
            working = False
            for char, j in zip(row, range(size)):
                if char == "#":
                    if not working:
                        continue
                    word_to_add = self.try_make_word_placement_from_string(word_string=current_word,
                                                                           starting_position=starting_position,
                                                                           direction=direction)
                    if word_to_add:
                        exported_word_placements.append(word_to_add)
                        word_to_add = None
                    current_word = ""
                    working = False
                else:
                    if not working:
                        starting_position = (
                            i, j) if direction == "Horizontal" else (j, i)
                        working = True
                    current_word = current_word + char
            word_to_add = self.try_make_word_placement_from_string(word_string=current_word,
                                                                   starting_position=starting_position,
                                                                   direction=direction)
            if word_to_add:
                exported_word_placements.append(word_to_add)
        return exported_word_placements

    def __fill_all_possible_word_places(self):
        size = self.__length
        two_dimensional_pattern = self.__pattern.rows
        self.__all_word_placements = []
        self.__all_word_placements.extend(self.ــfind_word_placements_of_2d_letters(
            two_dimensional_pattern=two_dimensional_pattern,
            size=size,
            direction="Horizontal"))

        two_dimensional_pattern = self.__pattern.cols
        self.__all_word_placements.extend(self.ــfind_word_placements_of_2d_letters(
            two_dimensional_pattern=two_dimensional_pattern,
            size=size,
            direction="Vertical"))

    def print_word_placements(self):
        for word in self.__all_word_placements:
            word.print_info()

    def get_pattern(self):
        return self.__pattern


def main():
    crossword = Crossword(pattern)
    crossword.get_pattern().draw()
    print()
    crossword.print_word_placements()


if __name__ == "__main__":
    main()
