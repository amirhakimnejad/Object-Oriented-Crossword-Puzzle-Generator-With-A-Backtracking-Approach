import random
import json
import datetime

RECURSION_MAX_ATTEMPTS = 100
accepted_characters_in_pattern = ['#', "_"]


class CrosswordPattern():
    cols = []
    rows = []
    size = 0

    def __init__(self, pattern_list, min_word_length=3, max_word_length=10):
        cols = []
        self.rows = [[char for char in row] for row in pattern_list]
        self.size = len(self.rows)

        if self.size < min_word_length:
            raise Exception(
                'Crossword pattern must have at least %s rows.' % min_word_length)
        if self.size > max_word_length:
            raise Exception(
                'Crossword pattern must have at most %s rows.' % max_word_length)
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
                        'Invalid crossword pattern, only %s are allowed not -%s-' % (','.join(accepted_characters_in_pattern), char))

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

    def __init__(self, starting_x, starting_y, direction, word_string, min_word_length=3, max_word_length=10):
        self.__letters = []
        
        self.__length = len(word_string)
        if self.__length < min_word_length or self.__length > max_word_length:
            raise Exception("Invalid word length")

        if not isinstance(direction, str):
            raise TypeError("direction must be set to a string")
        if direction not in ["Horizontal", "Vertical"]:
            raise ValueError(
                "direction must be either 'Horizontal' or 'Vertical'")

        if direction == "Horizontal" and (abs(starting_x - self.__length) > self.__length):
            raise Exception("Invalid horizontal word %s %s %s" % (
                starting_x, self.__length, word_string))
        if direction == "Vertical" and (abs(starting_y - self.__length) > self.__length):
            raise Exception("Invalid vertical word %s %s %s" %
                            (starting_x, self.__length, word_string))

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

    def get_object_cartesian(self):
        return {
            'startPosition': {
                "x": self.__starting_y,
                "y": self.__starting_x,
            },
            "direction": {'x': 1, 'y': 0} if self.__direction == "Horizontal" else {'x': 0, 'y': 1},
            "length": self.__length,
            "word": self.get_string()
        }


class Crossword():
    __all_word_placements = []
    __pattern = None
    __answers = []
    __solutions = []
    __length = -1

    def __init__(self, pattern, all_possible_answers, min_word_length=3, max_word_length=10):
        self.__all_word_placements = []
        self.__answers = []
        self.__solutions = []
        self.__pattern = CrosswordPattern(pattern)
        self.__length = self.__pattern.size
        self.__fill_all_possible_word_places()
        self.fill_answers(all_possible_answers, [
                          word for word in all_possible_answers], self.__answers)

    def fill_answers(self, all_possible_answers, available_possible_answers, answers_stack=[], attempts_tried=0):
        attempts_tried += 1
        if attempts_tried > RECURSION_MAX_ATTEMPTS:
            raise Exception("Too many attempts")

        if len(self.__all_word_placements) == len(answers_stack):
            return
        biggest_word_to_find = self.__all_word_placements[-len(
            answers_stack)-1]
        answer_to_add = CrossWordWord(biggest_word_to_find.get_x(), biggest_word_to_find.get_y(
        ), biggest_word_to_find.get_direction(), biggest_word_to_find.get_string())
        possible_answers = [word for word in available_possible_answers if len(
            word) == answer_to_add.get_length()]
        random.shuffle(possible_answers)
        for answer in possible_answers:
            answer_to_add.fill_word(answer)
            if self.can_coming_string_be_in_word_placement(answer_to_add, answer):
                available_possible_answers.remove(
                    answer_to_add.get_string())
                answers_stack.append(answer_to_add)
                available_possible_answers.extend([word for word in all_possible_answers if len(
                    word) < answer_to_add.get_length() and word not in available_possible_answers])
                return self.fill_answers(all_possible_answers, available_possible_answers, answers_stack, attempts_tried)
        if len(answers_stack) == 0:
            return
        answers_stack.pop()
        return self.fill_answers(all_possible_answers, available_possible_answers, answers_stack, attempts_tried)

    @staticmethod
    def try_make_word_placement_from_string(word_string, starting_position, direction):
        try:
            word = CrossWordWord(
                starting_x=starting_position[0], starting_y=starting_position[1], direction=direction, word_string=word_string)
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
    
    def get_list_of_required_letters_to_solve(self):
        required_letters = []
        for word in self.get_answers():
            all_letters_repeat = Counter(''.join(required_letters))
            word_string = word.get_string()
            word_with_letter_repeat = Counter(word_string)
            
            for letter in set(word_string):
                times_to_add = word_with_letter_repeat[letter] - all_letters_repeat[letter]
                if times_to_add <= 0:
                    continue
                for i in range(times_to_add):
                    required_letters.append(letter)
        return required_letters
        

    def print_word_placements(self):
        print("Required word placements:")
        for word in self.__all_word_placements:
            word.print_info()
    
    def get_answers(self):
        return self.__answers

    def get_pattern(self):
        return self.__pattern

    def print_answers(self):
        print("Answers:")
        for answer in self.get_answers():
            answer.print_info()

    def get_json_cartesian(self):
        level_data = {}
        level_data['wordData'] = [word.get_object_cartesian()
                                  for word in self.__answers]
        level_data['panLetters'] = self.get_list_of_required_letters_to_solve()
        return json.dumps(level_data)


def generate_crossword(pattern, all_possible_answers, min_word_length, max_word_length):
    crossword = Crossword(pattern, all_possible_answers, min_word_length, max_word_length)
    return crossword


def load_pattern(file_name):
    pattern = []
    pattern_file = open("patterns/%s" % file_name, "r").readlines()
    for line in pattern_file:
        pattern.append([char for char in line.strip()])
    return pattern


def load_random_pattern():
    pattern_name = "pattern%d.txt" % random.randint(1, 11)
    return load_pattern(pattern_name)


def load_words():
    words = [word.strip() for word in open("possible_words.txt",
                                           "r").readlines() if CrossWordWord.is_valid_string(word.strip())]

    unique_words = []
    for word in words:
        if word not in unique_words:
            unique_words.append(word)
    return unique_words


def create_levels_over_time(seconds_to_run, min_word_length, max_word_length):
    endTime = datetime.datetime.now() + datetime.timedelta(seconds=seconds_to_run)
    levels = []
    counter = 0
    while datetime.datetime.now() < endTime:
        try:
            levels.append(create_a_level(min_word_length, max_word_length))
            counter += 1
        except:
            pass
    if len(levels) <= 0:
        raise Exception("No levels created")
    print("Created %d levels" % counter)
    return levels


def create_levels(how_many_levels, min_word_length, max_word_length):
    levels = []
    tries = 0
    while len(levels) < how_many_levels or tries >= (how_many_levels * 2):
        try:
            levels.append(create_a_level(min_word_length, max_word_length))
        except:
            pass
        tries += 1
    if len(levels) <= 0:
        raise Exception("No levels created")
    print("Created %d levels" % len(levels))
    return levels


def create_a_level(min_word_length, max_word_length, pattern_to_use=None, words=None):
    max_tries = 10
    if words is None:
        all_possible_answers = load_words()
    else:
        all_possible_answers = words
    for i in range(max_tries):
        if pattern_to_use is None:
            pattern = load_random_pattern()
        else:
            pattern = pattern_to_use
        try:
            crossword = generate_crossword(pattern, all_possible_answers, min_word_length, max_word_length)
            return crossword
        except:
            continue
    raise Exception("Could not create a level after %d tries each with the depth of %s" % (
        max_tries, RECURSION_MAX_ATTEMPTS))


def create_json_from_levels_list(levels):
    levels_dict = {}
    for level, i in zip(levels, range(len(levels))):
        levels_dict[i] = json.loads(level.get_json_cartesian())
    return json.dumps(levels_dict)


def main():
    ## Create one level
    crossword_puzzle = create_a_level(min_word_length=3, max_word_length=6)
    crossword_puzzle.get_pattern().draw()
    crossword_puzzle.print_word_placements()
    crossword_puzzle.print_answers()
    print(crossword_puzzle.get_json_cartesian())
    
    ## Create max possible number of levels over time
    # levels = create_levels_over_time(seconds_to_run=5, min_word_length=3, max_word_length=10)
    # levels = create_json_from_levels_list(levels)
    # print(levels)
    
    ## Create a fixed number of levels
    # levels = create_levels(how_many_levels=10, min_word_length=3, max_word_length=10)
    # levels = create_json_from_levels_list(levels)
    # print(levels)


if __name__ == "__main__":
    main()
