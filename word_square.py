import random
from typing import Any

ALL_WORDS_DICTIONARY = {
    "a": []}  # This is dictionary that stores word based on the beginning

ALL_WORDS_LIST = []
POSSIBLE_WORDS = []
use = []


def words_maker():
    global ALL_WORDS_DICTIONARY
    if len(ALL_WORDS_DICTIONARY) > 1:
        return ALL_WORDS_DICTIONARY
    
    text = open("wordes.txt", "r")

    for line in text:
        word = line.lower().replace("\n", "")
        if not (len(word) == 0 or "abbr." in word or " prefix " in word):
            ALL_WORDS_DICTIONARY.setdefault(word[0], [])
            word = word[:word.find(" ")]
            letter = 0
            while letter < len(word):
                if letter in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                              "-", "'", '"']:
                    word = word[:letter] + word[letter + 1:]
                    letter -= 1
                letter += 1

            if len(word) > 0 and word not in ALL_WORDS_DICTIONARY[word[0]]:
                ALL_WORDS_DICTIONARY[word[0]].append(word)
                
    text.close()
    
    return ALL_WORDS_DICTIONARY


def make_word_list() -> list[str]:
    global ALL_WORDS_LIST
    if len(ALL_WORDS_LIST) > 1:
        return ALL_WORDS_LIST

    text = open("wordes.txt", "r")

    for line in text:
        word = line.lower().replace("\n", "")
        if not (len(word) == 0 or "abbr." in word or " prefix " in word):

            word = word[:word.find(" ")]
            letter = 0
            while letter < len(word):
                if letter in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                              "-", "'", '"']:
                    word = word[:letter] + word[letter + 1:]
                    letter -= 1
                letter += 1

            if len(word) > 0 and word not in ALL_WORDS_LIST:
                ALL_WORDS_LIST.append(word)

    text.close()

    return ALL_WORDS_DICTIONARY


def used(word: str, uses: list) -> list:
    for i in word:
        if i not in uses:
            uses.append(i)
    return uses


def find_best(letters: list[str]):
    lst = []
    letters = letters
    for i in letters:
        lst.append(find_helper(i, letters, []))
        print(i)
    return lst


def find_helper(first_letter: str, letters: list[str], words_used: list[str],
                letters_used=[]) -> list[str]:
    if len(letters_used) >= len(letters):
        return [""]
    else:
        lst = []
        __words = word_find(first_letter, letters)
        for wor in __words:
            # print(word)
            if len(wor) >= 4 and wor[0] != wor[-1] and wor not in words_used:
                lst.append(wor)
                lst.append([find_helper(wor[-1], letters, [wor] + words_used,
                                        used(wor, letters_used))])

        return lst


def word_find(first_letter: str, letter_lst: list[str], letters_used=[]) -> \
        list[str]:
    if len(ALL_WORDS_DICTIONARY) == 1:
        words_maker()

    # first_letter = input("first letter? ")

    # letters = input("Letters?")

    # letter_lst = letters.strip().split(', ')

    l1 = letter_lst[:3]
    l2 = letter_lst[3:6]
    l3 = letter_lst[6:9]
    l4 = letter_lst[9:]

    # letter_lst.append(first_letter)

    word_lst = []

    for word in ALL_WORDS_DICTIONARY[first_letter]:
        a = True
        i = 0
        while i < len(word) - 1:
            if word[i] not in letter_lst:
                a = False
            elif word[i] in l1 and word[i + 1] in l1:
                a = False
            elif word[i] in l4 and word[i + 1] in l4:
                a = False
            elif word[i] in l2 and word[i + 1] in l2:
                a = False
            elif (word[i] in l3 and word[i + 1] in l3) or word[i] == word[
                i + 1]:
                a = False
            i += 1

        if a and len(word) > 0 and word[-1] in letter_lst:
            word_lst.append(word)

    return word_lst


def longest_word(lst: list[str]):
    j = 0
    i = 0
    while j < len(lst):
        if len(lst[j]) > len(lst[i]):
            i = j
        j += 1

    return lst[i]


def spelling_bee(letters: list[str]) -> list[str]:
    if len(ALL_WORDS_DICTIONARY) == 1:
        words_maker()

    word_lst = []
    for first_letter in letters:
        for word in ALL_WORDS_DICTIONARY[first_letter]:
            a = True
            if letters[0] not in word or len(word) <= 3:
                a = False
            else:
                for letter in word:
                    if letter not in letters:
                        a = False
            if a:
                word_lst.append(word)

    return word_lst


def word_finder(first_letter: str, letters: list[str]) -> list[str]:
    if len(ALL_WORDS_DICTIONARY) == 1:
        words_maker()

    possible_words = ALL_WORDS_DICTIONARY[first_letter]
    final_words = []
    for word in possible_words:
        a = True
        for i in range(1, len(word)):

            if i == len(word) - 1 and word[i] not in letters:
                a = False
            elif word[i] in letters[:3] and word[i - 1] in letters[:3]:
                a = False
            elif word[i] in letters[3:6] and word[i - 1] in letters[3:6]:
                a = False
            elif word[i] in letters[6:9] and word[i - 1] in letters[6:9]:
                a = False
            elif word[i] in letters[9:] and word[i - 1] in letters[9:]:
                a = False
            elif word[i] not in letters:
                a = False

        if a:
            final_words.append(word)
    return final_words


def _create_unvisited_node(word_square_letter_list: list[str]):
    possible_words = _make_word_square_words(word_square_letter_list)
    unvisited = {}
    for word in possible_words:
        unvisited[word] = float('inf')

    return unvisited


def _word_square(word_square_letter_list: list[str]):
    unvisited = _create_unvisited_node(word_square_letter_list)
    start_word = random.choice(unvisited)

    unvisited[start_word] = 0


def _get_all_possible_words(word_square_letter_list: list[str]):
    if len(ALL_WORDS_DICTIONARY) == 1:
        words_maker()
    possible_word_dict = dict()
    for first_letter in word_square_letter_list:
        possible_words = ALL_WORDS_DICTIONARY[first_letter]

        for word in possible_words:
            a = True
            for i in range(1, len(word)):

                if i == len(word) - 1 and word[i] not in word_square_letter_list:
                    a = False

                elif (word[i] in word_square_letter_list[:3]
                      and word[i - 1] in word_square_letter_list[:3]):
                    a = False

                elif (word[i] in word_square_letter_list[3:6]
                      and word[i - 1] in word_square_letter_list[3:6]):
                    a = False

                elif (word[i] in word_square_letter_list[6:9]
                      and word[i - 1] in word_square_letter_list[6:9]):
                    a = False

                elif (word[i] in word_square_letter_list[9:]
                      and word[i - 1] in word_square_letter_list[9:]):
                    a = False

                elif word[i] not in word_square_letter_list:
                    a = False

            if a:
                possible_word_dict.setdefault(word[-1], word)

    return possible_word_dict



def _make_word_square_words(word_square_letter_list: list[str]):

    possible_word_list = []
    # for lett in word_square_letter_list:
    #
    #
    # return possible_word_list




def word_square(letters: list[str]) -> list[str]:
    list_of_words = [flwil(word_finder(random.choice(letters), letters))]
    _word_square_helper(list_of_words, letters)
    return list_of_words


def _word_square_helper(list_of_words, letters, length=2, attempts=0):
    if len(list_of_words) < length:
        posippl_words = word_finder(list_of_words[-1][-1], letters)
        smth = flwil(posippl_words)
        while smth in list_of_words:
            smth = flwil(posippl_words)
        list_of_words.append(smth)
        _word_square_helper(list_of_words, letters, length)

    letter_tracker = letters + []

    for i in list_of_words:
        for lett in i:
            if lett in letter_tracker:
                letter_tracker.remove(lett)
    a = True
    if 0 < len(letter_tracker) < 3:
        posippl_words = word_finder(list_of_words[-1][-1], letters)
        for the_words in posippl_words:
            if (letter_tracker[-1] in the_words and
                    letter_tracker[0] in the_words):
                list_of_words.append(the_words)
                a = False
    if a and len(letter_tracker) > 0 and length in range(2, 7):
        while len(list_of_words) > 0:
            list_of_words.pop()
        list_of_words.append(
            flwil(word_finder(random.choice(letters), letters)))
        attempts += 1
        if attempts > len(letters) * 2:
            _word_square_helper(list_of_words, letters, length + 1, 0)
        else:
            _word_square_helper(list_of_words, letters, length + 1,
                                attempts + 1)


def best_possible_outcome(letters: list[str]):
    lst = []
    for i in range(100):
        lst.append(word_square(letters))

    return find_min_length(lst)


def flwil(lst: list[str]):
    index = 0
    a = 0

    for i in range(len(lst)):
        if len(lst[i]) >= a:
            a = len(lst[i])
            index = i
    return lst.pop(index)


def find_min_length(lst: list):
    index = 0
    a = 1000
    for i in range(len(lst)):
        if len(lst[i]) < a:
            a = len(lst[i])
            index = i

    return lst[index]

def run_word_square():
    row = 0
    letter_list = []
    while row < 4:
        letters = input(f'Enter the values of the {row + 1}th row\n'
                   f'(separated letters by commas): ')

        letters = letters.split(',')
        for lett in letters:
            lett = lett.strip()
            letter_list.append(lett)

        row += 1

    best_strat = []
    a = float('inf')
    for i in range(100):
        strat = word_square(letter_list)
        if a > len(strat) > 0:
            a = len(strat)
            best_strat = strat

    return best_strat


print(run_word_square())

