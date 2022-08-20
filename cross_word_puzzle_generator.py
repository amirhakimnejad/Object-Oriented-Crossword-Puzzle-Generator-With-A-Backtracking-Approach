import random

MinimumAcceptedLength = 3
MaximumAcceptedLength = 10

accepted_characters_in_pattern = ['#', "_"]


class CrosswordPattern():
    cols = []
    rows = []
    size = 0

    def __init__(self, pattern_list):
        self.rows = [[char for char in row] for row in pattern_list]
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
                        'Invalid crossword pattern, only \'#\' and \'ـ\' are allowed - %s' % char)

        if len(self.cols) != self.size:
            raise Exception(
                'Invalid crossword pattern, each column must have the same length')

        self.check_if_pattern_is_valid()

    # TODO: check if all possible words are legal.
    def check_if_pattern_is_valid(self):
        pass

    def draw(self, direction='Horizontal'):
        print('Pattern:')
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
            raise Exception('Invalid character "%s"' % character)

        self.__character = character
        self.x = x
        self.y = y

    def is_filled(self):
        return self.__character != "_" and self.__character != ''

    def is_found(self):
        return is_alpha(self.__character)

    def is_block(self):
        return self.__character == '#'

    def get_character(self):
        return self.__character

    def get_index(self):
        return (self.x, self.y)

    def print_info(self):
        print('%s at %s, %s' %
              (self.__character, self.get_index()[0], self.get_index()[1]))


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
            word_string = "_" * self.__length
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
                    letter, self.__starting_x, self.__starting_y + i))
            elif self.__direction == "Vertical":
                self.__letters.append(CrossWordLetter(
                    letter, self.__starting_x + i, self.__starting_y))
            else:
                raise Exception("Invalid direction")

        for i in range(self.__length):
            if self.__direction == "Horizontal":
                if self.__letters[i].get_index()[0] != self.__starting_x:
                    raise Exception("Invalid horizontal word")
                if self.__letters[i].get_index()[1] != self.__starting_y + i:
                    raise Exception("Invalid horizontal word")
            elif self.__direction == "Vertical":
                if self.__letters[i].get_index()[0] != self.__starting_x + i:
                    raise Exception("Invalid vertical word")
                if self.__letters[i].get_index()[1] != self.__starting_y:
                    raise Exception("Invalid vertical word")

        if '#' in self.__letters:
            raise Exception("Invalid placement of word")

        if not isinstance(self.__letters, type([CrossWordLetter])):
            raise TypeError("letters must be set to a list")

        if len(word_string) != len(self.__letters):
            raise Exception("Invalid word length")

    def empty_word(self):
        self.fill_word("_" * self.__length)

    def is_filled_letters_match_coming_word(self, other_word):
        for letter in self.__letters:
            other_letter = other_word.try_get_letter_with_index(
                letter.get_index())
            if other_letter is None:
                continue
            if other_letter.get_character() != letter.get_character():
                return False
        return True

    def get_length(self):
        return self.__length

    def get_string(self):
        return ''.join([letter.get_character() for letter in self.__letters])

    def try_get_letter_with_index(self, index):
        for letter in self.__letters:
            if letter.get_index() == index:
                return letter
        return None

    def get_x(self):
        return self.__starting_x

    def get_y(self):
        return self.__starting_y

    def get_direction(self):
        return self.__direction

    @staticmethod
    def is_valid_string(string):
        return len([char for char in string if not CrossWordLetter.is_valid_character(char)]) <= 0

    def print_info(self):
        print("------------------------------")
        print("Word: %s" % [letter.get_character()
              for letter in self.__letters])
        for letter in self.__letters:
            letter.print_info()
        print("Starting x: %s" % self.__starting_x)
        print("Starting y: %s" % self.__starting_y)
        print("Direction: %s" % self.__direction)
        print("Length: %s" % self.__length)
        print("Filled: %s" % self.is_filled())
        print("------------------------------")


class Crossword():
    __all_word_placements = []
    __pattern = None
    __answers = []
    __solutions = []
    __length = -1

    def __init__(self, pattern, all_possible_answers):
        self.__pattern = CrosswordPattern(pattern)
        self.__length = self.__pattern.size
        self.__fill_all_possible_word_places()
        self.fill_answers(all_possible_answers,
                          [word for word in all_possible_answers], self.__answers)

    def fill_answers(self, all_possible_answers, available_possible_answers, answers_stack=[]):
        if len(self.__all_word_placements) == len(answers_stack):
            return
        biggest_word_to_find = self.__all_word_placements[-len(
            answers_stack)-1]
        answer_to_add = CrossWordWord(biggest_word_to_find.get_x(), biggest_word_to_find.get_y(
        ), biggest_word_to_find.get_direction(), biggest_word_to_find.get_length())
        possible_answers = [word for word in available_possible_answers if len(
            word) == answer_to_add.get_length()]
        for answer in possible_answers:
            answer_to_add.fill_word(answer)
            if self.can_coming_string_be_in_word_placement(answer_to_add, answer):
                available_possible_answers.remove(
                    answer_to_add.get_string())
                answers_stack.append(answer_to_add)
                available_possible_answers.extend([word for word in all_possible_answers if len(
                    word) < answer_to_add.get_length() and word not in available_possible_answers])
                return self.fill_answers(all_possible_answers, available_possible_answers, answers_stack)
        if len(answers_stack) == 0:
            return
        answers_stack.pop()
        return self.fill_answers(all_possible_answers, available_possible_answers, answers_stack)

    @staticmethod
    def try_make_word_placement_from_string(word_string, starting_position, direction):
        try:
            word = CrossWordWord(
                starting_x=starting_position[0], starting_y=starting_position[1], direction=direction, length=len(word_string))
            return word
        except Exception as e:
            return None

    def can_coming_string_be_in_word_placement(self, word_placement_to_fill, word_string):
        for answer in self.__answers:
            if not answer.is_filled_letters_match_coming_word(word_placement_to_fill):
                return False
        return True

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
                    word_to_add = Crossword.try_make_word_placement_from_string(word_string=current_word,
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
            word_to_add = Crossword.try_make_word_placement_from_string(word_string=current_word,
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

        self.__all_word_placements.sort(
            key=lambda x: x.get_length(), reverse=False)

    def print_word_placements(self):
        print("Required word placements:")
        for word in self.__all_word_placements:
            word.print_info()

    def get_pattern(self):
        return self.__pattern

    def print_answers(self):
        print("Answers:")
        for answer in self.__answers:
            answer.print_info()


def generate_puzzle(pattern, all_possible_answers):
    random.shuffle(all_possible_answers)
    crossword = Crossword(pattern, all_possible_answers)
    return crossword


def load_pattern(file_name):
    pattern = []
    pattern_file = open("patterns/%s" % file_name, "r").readlines()
    for line in pattern_file:
        pattern.append([char for char in line.strip()])
    return pattern


def load_words():
    words = [word.strip() for word in open("possible_words.txt",
                                           "r").readlines() if CrossWordWord.is_valid_string(word.strip())]
    return list(set(words))


def main():
    pattern = load_pattern("pattern1.txt")
    words_list = load_words()
    crossword_puzzle = generate_puzzle(pattern, words_list)
    crossword_puzzle.get_pattern().draw()
    crossword_puzzle.print_word_placements()
    crossword_puzzle.print_answers()


if __name__ == "__main__":
    main()
