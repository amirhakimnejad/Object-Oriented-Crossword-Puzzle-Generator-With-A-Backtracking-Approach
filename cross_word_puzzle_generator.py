import random
import json
import datetime
from collections import Counter

SORT_WITH_SIMILARITY = True
accepted_characters_in_pattern = ['#', "_"]
MINIMUM_SUPPORTED_LENGTH = 3
MAXIMUM_SUPPORTED_LENGTH = 10


def find_number_of_character_repeat_of_a_string_in_another(word1, word2):
    count = 0
    for char in word1:
        if char in word2:
            count += 1
    return count


def validate_word_for_pattern(word_string, starting_position, direction):
    length = len(word_string)
    if length < MINIMUM_SUPPORTED_LENGTH or length > MAXIMUM_SUPPORTED_LENGTH:
        raise Exception("Invalid word length")

    if not isinstance(direction, str):
        raise TypeError("direction must be set to a string")
    if direction not in ["Horizontal", "Vertical"]:
        raise ValueError(
            "direction must be either 'Horizontal' or 'Vertical'")


class CrosswordPattern():
    __mock_words = []
    __cols = []
    __rows = []
    __size = 0

    def __init__(self, pattern_list):
        self.__rows = [[char for char in row] for row in pattern_list]
        self.__size = len(self.__rows)

        if self.__size < MINIMUM_SUPPORTED_LENGTH:
            raise Exception(
                'Crossword pattern must have at least %s rows.' % MINIMUM_SUPPORTED_LENGTH)
        if self.__size > MAXIMUM_SUPPORTED_LENGTH:
            raise Exception(
                'Crossword pattern must have at most %s rows.' % MAXIMUM_SUPPORTED_LENGTH)
        self.__cols = [[self.__rows[j][i] for j in range(
            len(self.__rows))] for i in range(len(self.__rows[0]))]

        for row in self.__rows:
            if len(self.__rows) != self.__size:
                raise Exception(
                    'Invalid crossword pattern, each row must have the same length')
            for char in row:
                if char not in accepted_characters_in_pattern:
                    raise Exception(
                        'Invalid crossword pattern, only %s are allowed not -%s-' % (','.join(accepted_characters_in_pattern), char))

        if len(self.__cols) != self.__size:
            raise Exception(
                'Invalid crossword pattern, each column must have the same length')

        self.update_list_of_word_placements()

    def get_size(self):
        return self.__size

    def update_list_of_word_placements(self):
        two_dimensional_pattern = self.__rows
        self.__mock_words = []
        self.__mock_words.extend(self.make_list_of_word_placements_of_2d_grid(
            two_dimensional_pattern=two_dimensional_pattern,
            size=self.__size,
            direction="Horizontal"))

        two_dimensional_pattern = self.__cols
        self.__mock_words.extend(self.make_list_of_word_placements_of_2d_grid(
            two_dimensional_pattern=two_dimensional_pattern,
            size=self.__size,
            direction="Vertical"))

    def get_mock_words(self):
        return self.__mock_words

    def make_list_of_word_placements_of_2d_grid(self, two_dimensional_pattern, size, direction):
        exported_word_placements = []

        for row, i in zip(two_dimensional_pattern, range(size)):
            current_word = ""
            starting_position = (-1, -1)
            working = False
            for char, j in zip(row, range(size)):
                if char == "#":
                    if not working:
                        continue
                    if len(current_word) > 1:
                        exported_word_placements.append(CrossWordWord(
                            word_string=current_word, starting_position=starting_position, direction=direction))
                    current_word = ""
                    working = False
                else:
                    if not working:
                        starting_position = (
                            i, j) if direction == "Horizontal" else (j, i)
                        working = True
                    current_word = current_word + char
            if len(current_word) > 1:
                exported_word_placements.append(CrossWordWord(
                    word_string=current_word, starting_position=starting_position, direction=direction))
        return exported_word_placements

    def draw(self, direction='Horizontal'):
        print('Pattern:')
        matrix_to_draw = [[]]
        if direction == 'Horizontal':
            matrix_to_draw = self.__rows
        elif direction == 'Vertical':
            matrix_to_draw = self.__cols
        else:
            raise Exception('Invalid direction')
        for row in matrix_to_draw:
            print(row)


class CrossWordLetter():
    __character = ''
    x = -1
    y = -1

    def __init__(self, character, x, y):
        if not CrossWordLetter.is_valid_character(character):
            raise Exception('Invalid character "%s"' % character)

        self.__character = character
        self.x = x
        self.y = y

    @staticmethod
    def is_valid_character(character):
        return character.isalpha() or character in accepted_characters_in_pattern

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
    __indexed_string = ''

    def __init__(self, starting_position, direction, word_string):
        self.__indexed_string = ''
        self.__letters = []

        validate_word_for_pattern(word_string, starting_position, direction)

        length = len(word_string)
        self.__length = length
        self.__direction = direction

        starting_x = starting_position[0]
        starting_y = starting_position[1]

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
        is_mock = False
        if word_string is None or word_string == "_" * self.__length:
            is_mock = True
        if word_string is None:
            word_string = "_" * self.__length
        self.fill_word(word_string=word_string, is_mock=is_mock)
        self.__indexed_string = self.__get_string()

    def is_filled(self):
        for letter in self.__letters:
            if not letter.is_filled():
                return False
        return True

    def fill_word(self, word_string, is_mock=True):
        if not is_mock:
            if not word_string.isalpha():
                raise Exception("Invalid word %s" % word_string)

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

        self.__indexed_string = self.__get_string()

    def empty_word(self):
        self.fill_word(word_string=("_" * self.__length), is_mock=True)

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

    @staticmethod
    def print_words_info(words):
        for word in words:
            word.print_info()

    def __get_string(self):
        return ''.join([letter.get_character() for letter in self.__letters])

    def try_get_letter_with_index(self, index):
        for letter in self.__letters:
            if letter.get_index() == index:
                return letter
        return None

    def get_starting_position(self):
        return (self.__starting_x, self.__starting_y)

    def get_direction(self):
        return self.__direction

    def indexed_string(self):
        return self.__indexed_string

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

    def get_object_cartesian(self):
        return {
            'startPosition': {
                "x": self.__starting_y,
                "y": self.__starting_x,
            },
            "direction": {'x': 1, 'y': 0} if self.__direction == "Horizontal" else {'x': 0, 'y': 1},
            "length": self.__length,
            "word": self.indexed_string()
        }


class Crossword():
    __sorted_words_placements = []
    __pattern = None
    __answers = []
    __solutions = []
    __length = -1

    def __init__(self, pattern, all_possible_answers):
        self.__sorted_words_placements = []
        self.__answers = []
        self.__solutions = []
        self.__pattern = pattern
        self.__length = self.__pattern.get_size()
        self.__sorted_words_placements = [
            word for word in self.__pattern.get_mock_words()]
        self.__sorted_words_placements.sort(
            key=lambda x: x.get_length(), reverse=False)
        self.fill_answers(all_possible_answers,
                          [word for word in all_possible_answers], self.__answers)

    def fill_answers(self, all_possible_answers, available_possible_answers, answers_stack=[]):
        if len(self.__sorted_words_placements) == len(answers_stack):
            return
        biggest_word_to_find = self.__sorted_words_placements[-len(
            answers_stack)-1]
        answer_to_add = CrossWordWord(biggest_word_to_find.get_starting_position(
        ), biggest_word_to_find.get_direction(), biggest_word_to_find.indexed_string())
        possible_answers = [word for word in available_possible_answers if len(
            word) == answer_to_add.get_length()]
        random.shuffle(possible_answers)
        if len(answers_stack) > 0 and SORT_WITH_SIMILARITY:
            possible_answers.sort(key=lambda word: find_number_of_character_repeat_of_a_string_in_another(
                answers_stack[-1].indexed_string(), word), reverse=True)
        for answer in possible_answers:
            answer_to_add.fill_word(word_string=answer, is_mock=False)
            if self.can_coming_string_be_in_word_placement(answer_to_add, answer):
                available_possible_answers.remove(
                    answer_to_add.indexed_string())
                answers_stack.append(answer_to_add)
                available_possible_answers.extend([word for word in all_possible_answers if len(
                    word) < answer_to_add.get_length() and word not in available_possible_answers])
                return self.fill_answers(all_possible_answers, available_possible_answers, answers_stack)
        if len(answers_stack) == 0:
            return
        answers_stack.pop()
        return self.fill_answers(all_possible_answers, available_possible_answers, answers_stack)

    def can_coming_string_be_in_word_placement(self, word_placement_to_fill, word_string):
        for answer in self.__answers:
            if not answer.is_filled_letters_match_coming_word(word_placement_to_fill):
                return False
        return True

    def get_list_of_required_letters_to_solve(self):
        required_letters = []
        for word in self.get_answers():
            all_letters_repeat = Counter(''.join(required_letters))
            word_string = word.indexed_string()
            word_with_letter_repeat = Counter(word_string)

            for letter in set(word_string):
                times_to_add = word_with_letter_repeat[letter] - \
                    all_letters_repeat[letter]
                if times_to_add <= 0:
                    continue
                for i in range(times_to_add):
                    required_letters.append(letter)
        return required_letters

    def get_answers(self):
        return self.__answers

    def get_pattern(self):
        return self.__pattern

    def get_json_cartesian(self):
        level_data = {}
        level_data['wordData'] = [word.get_object_cartesian()
                                  for word in self.__answers]
        level_data['panLetters'] = self.get_list_of_required_letters_to_solve()
        return json.dumps(level_data)


def load_pattern(file_name):
    pattern = []
    pattern_file = open("patterns/%s" % file_name, "r").readlines()
    for line in pattern_file:
        pattern.append([char for char in line.strip()])
    return pattern


def load_random_pattern():
    pattern_name = "pattern%d.txt" % random.randint(1, 10)
    return load_pattern(pattern_name)


def load_words():
    words = [word.strip() for word in open("possible_words.txt",
                                           "r").readlines() if CrossWordWord.is_valid_string(word.strip())]
    words = [word.upper() for word in words]
    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return unique_words


def create_levels_over_time(seconds_to_run):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds_to_run)
    levels = []
    counter = 0
    while datetime.datetime.now() < endTime:
        try:
            levels.append(create_a_level())
            counter += 1
        except:
            pass
    if len(levels) <= 0:
        raise Exception("No levels created")
    print("Created %d levels" % counter)
    return levels


def create_levels_with_maximum_length(how_many_levels, maximum_length=None):
    levels = []
    while len(levels) < how_many_levels:
        try:
            created_level = create_a_level()
            if not maximum_length is None and len(created_level.get_list_of_required_letters_to_solve()) >= maximum_length:
                continue
            levels.append(created_level)
            print("Created level %d" % len(levels))
        except:
            continue
    if len(levels) <= 0:
        raise Exception("No levels created")
    print("Created %d levels" % len(levels))
    return levels


def create_a_level(pattern_to_use=None, words=None):
    max_tries = 10
    exceptions_text = []
    if words is None:
        all_possible_answers = load_words()
    else:
        all_possible_answers = words
    for i in range(max_tries):
        if pattern_to_use is None:
            pattern = CrosswordPattern(load_random_pattern())
        else:
            pattern = pattern_to_use
        try:
            crossword = Crossword(pattern, all_possible_answers)
            return crossword
        except Exception as e:
            exceptions_text.append(str(e))
            continue
    raise Exception("Could not create a level after %d tries, reported reasons are %s" % (
        max_tries, exceptions_text))


def create_json_from_levels_list(levels):
    levels_dict = {}
    for level, i in zip(levels, range(len(levels))):
        levels_dict[i] = json.loads(level.get_json_cartesian())
    return json.dumps(levels_dict)


def save_dictionary_as_json_file(dictionary, file_name):
    file = open('levels/%s.json' % file_name, 'w')
    file.write(json.dumps(dictionary))


def save_dictionaries_as_json_files(dictionaries):
    for dictionary, i in zip(dictionaries, range(1, len(dictionaries))):
        save_dictionary_as_json_file(dictionary, 'level%s' % i)

def test_all_patterns():
    for i in range(1, 11):
        pattern = CrosswordPattern(load_pattern("pattern%d.txt" % i))

def test_all_word_placements():
    placements = []
    for i in range(1, 11):
        pattern = CrosswordPattern(load_pattern("pattern%d.txt" % i))
        placements.extend(pattern.get_mock_words())

def main():
    # test_all_patterns()
    # test_all_word_placements()
    # Create one level
    crossword_puzzle = create_a_level()
    crossword_puzzle.get_pattern().draw()
    CrossWordWord.print_words_info(crossword_puzzle.get_pattern().get_mock_words())
    CrossWordWord.print_words_info(crossword_puzzle.get_answers())
    print(crossword_puzzle.get_json_cartesian())

    # Create max possible number of levels over time
    # levels = create_levels_over_time(4)
    # levels = create_json_from_levels_list(levels)
    # print(levels)

    # Create a fixed number of levels
    # levels = create_levels_with_maximum_length(2, 7)
    # levels = create_json_from_levels_list(levels)
    # print(levels)


if __name__ == "__main__":
    main()
