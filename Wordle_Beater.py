import math
import random
import matplotlib.pyplot as plt
import threading

five_letter_words = []
generalWordFrequency = {}


def five_letter_word_maker():
    text = open("words.txt", "r")
    global generalWordFrequency
    CreateGeneralWordFrequency()

    global five_letter_words
    if len(five_letter_words) > 1:
        return five_letter_words
    for line in text:
        word = line.lower().replace("\n", "")
        word = word.strip("'")

        if not (len(word) == 0 or "abbr." in word or " prefix " in word):
            word = word[:word.find(" ")]

            letter = 0
            while letter < len(word):
                if word[letter] in ["1", "2", "3", "4", "5", "6", "7", "8", "9",
                                    "0",
                                    "-", "'", '"']:
                    word = word[:letter] + word[letter + 1:]
                    letter -= 1
                letter += 1

            if (len(word) == 5 and word not in five_letter_words
                    and word in generalWordFrequency):
                five_letter_words.append(word)

            # if (len(word) == 4 and (word + 's') not in five_letter_words
            #         and word + 's' in generalWordFrequency):
            #     five_letter_words.append(word + 's')
    return five_letter_words


def CreateGeneralWordFrequency() -> None:
    global generalWordFrequency

    if len(generalWordFrequency) > 1:
        return None
    fiveLetterWordFrequencyFile = open('archive/fiveLetterWordFrequency.csv'
                                       , 'r', newline="\n")

    for line in fiveLetterWordFrequencyFile:
        line = line.split(',')
        generalWordFrequency[line[0]] = float(line[1].strip())

    return None


def words_letters_at_pos(pos: int, words=None) -> dict[str, list[str]]:
    words_dic = {}
    all_words = words
    if all_words is None:
        all_words = five_letter_word_maker()

    for word in all_words:
        words_dic.setdefault(word[pos], [])
        words_dic[word[pos]].append(word)

    return words_dic


def intersect_dictionary(d1: dict[str, list[str]],
                         d2: dict[str, list[str]]) -> list[str]:
    l1 = []
    l2 = []

    for key in d1:
        for word in d1[key]:
            l1.append(word)

    for key in d2:
        for word in d2[key]:
            l2.append(word)

    return intersect_list(l1, l2)


def intersect_list(l1: list[str], l2: list[str]) -> list[str]:
    lst = []

    for word in l1:
        if word in l2:
            lst.append(word)

    return lst


def remove_key_from_dic(d1: dict, key) -> None:
    if key in d1:
        d1.pop(key)


def remove_all_but_one_key(d1: dict, key) -> dict:
    return {key: d1[key]}


def new_wordle():
    WelcomeText = ("Welcome to the Wordle Beater.\n "
                   "You will be shortly prompted to enter your first guessed"
                   "letter into the terminal.\n"
                   "\nNext you will be prompted to input the status of each "
                   "letter in your guessed word.\n"
                   "\t Input -1 if the letter is NOT in the correct word\n"
                   "\t Input 0 if the letter IS in the correct word at the "
                   "correct position.\n"
                   "\t Input 1 if the letter IS in the correct word at the "
                   "INCORRECT position.\n\n")
    print(WelcomeText)
    portionedLetter = [words_letters_at_pos(0), words_letters_at_pos(1),
                       words_letters_at_pos(2), words_letters_at_pos(3),
                       words_letters_at_pos(4)]

    print("First Recommended Word: ", calculate_new_next_best_word(
        portionedLetter))
    guess = input("First Guessed word:")
    guess = guess.strip().lower()

    l5 = _new_wordle_helper(portionedLetter, guess)

    # print("Recommended next word: ", calculate_next_best_word(portionedLetter,
    #                                                           l5))

    print("Recommended next word: ", calculate_new_next_best_word(
        portionedLetter))

    num_guesses = 2
    while len(l5) > 1 and num_guesses < 6:
        print("Guess", num_guesses, " out of 6")
        guess = input("Guessed word:")
        guess = guess.strip().lower()
        if len(guess) == 5:
            l5 = _new_wordle_helper(portionedLetter, guess)

            print("Recommended next word: ",
                  calculate_new_next_best_word(portionedLetter))
            num_guesses += 1
        else:
            print("Invalid Word Entry")

    return l5


def _new_wordle_helper(list_of_dicts, guess):
    repeated_letters = find_word_duplicate_letters(guess)
    repeated_letters_status = {}

    for i in range(len(list_of_dicts)):

        letterStatus = input(f'Status of Letter {guess[i]}:')
        while letterStatus not in ['0', '1', '-1']:
            letterStatus = input(f'Status of Letter {guess[i]}:')
        if guess[i] in repeated_letters:
            repeated_letters_status.setdefault(guess[i], [])
            repeated_letters_status[guess[i]].append((i, letterStatus))

        if letterStatus == '0':
            list_of_dicts[i] = remove_all_but_one_key(list_of_dicts[i],
                                                      guess[i])

        elif letterStatus == '1':
            remove_key_from_dic(list_of_dicts[i], guess[i])

        elif letterStatus == '-1' and guess[i] not in repeated_letters:
            for j in range(len(list_of_dicts)):
                remove_key_from_dic(list_of_dicts[j], guess[i])

    _new_wordle_deal_with_duplicate_letters(list_of_dicts,
                                            repeated_letters_status)

    l5 = _update_list_of_dicts(list_of_dicts)

    return l5


def _update_list_of_dicts(list_of_dicts):
    l1 = intersect_dictionary(list_of_dicts[0], list_of_dicts[1])
    l2 = intersect_dictionary(list_of_dicts[2], list_of_dicts[3])
    l3 = intersect_dictionary(list_of_dicts[4], list_of_dicts[4])

    l4 = intersect_list(l1, l2)
    l5 = intersect_list(l3, l4)

    #
    list_of_dicts[0] = words_letters_at_pos(0, l5)
    list_of_dicts[1] = words_letters_at_pos(1, l5)
    list_of_dicts[2] = words_letters_at_pos(2, l5)
    list_of_dicts[3] = words_letters_at_pos(3, l5)
    list_of_dicts[4] = words_letters_at_pos(4, l5)

    return l5


def _new_wordle_deal_with_duplicate_letters(list_of_dicts,
                                            repeated_letters_status):
    for letter, status in repeated_letters_status.items():
        letterStatus = '-1'

        for tup in status:
            if tup[1] == '0':
                letterStatus = '0'
                list_of_dicts[tup[0]] = remove_all_but_one_key(
                    list_of_dicts[tup[0]], letter)

            elif tup[1] == '1':
                letterStatus = '1'
                remove_key_from_dic(list_of_dicts[tup[0]], letter)

            elif tup[1] == '-1':
                remove_key_from_dic(list_of_dicts[tup[0]], letter)

        if letterStatus == '-1':
            for j in range(len(list_of_dicts)):
                remove_key_from_dic(list_of_dicts[j], letter)


def curve(x: float) -> float:
    a = .5
    b = .01
    return math.exp(-1 * ((x - a) ** 2) / b)


def calculate_new_next_best_word(lst: list[dict[str, list[str]]]) -> str:
    CreateGeneralWordFrequency()

    frequency_of_word = {}
    most_common_word = ("", float('-inf'))
    # total_length_of_dictionary_values = 0

    for dictionary in lst:
        for letter in dictionary:
            for word in dictionary[letter]:
                frequency_of_word.setdefault(word, 0)
                frequency_of_word[word] += len(dictionary[letter])
                # total_length_of_dictionary_values += len(dictionary[letter])

    for word in frequency_of_word:

        repeated_letters = find_word_duplicate_letters(word)

        # curved_frequency_score = curve(
        #     frequency_of_word[word] / total_length_of_dictionary_values)

        # score = curved_frequency_score * (1 - (
        #         len(repeated_letters) * 2 / len(word)))

        # if word == 'cross':
        #     print("cross")
        #
        score = frequency_of_word[word] * (1 - (
                len(repeated_letters) * 2.0 / len(word)))

        if word[-1] == 's':
            score /= 2

        if word in generalWordFrequency:
            score *= generalWordFrequency[word]
        else:
            score *= 0

        if score > most_common_word[1]:
            most_common_word = (word, score)

    return most_common_word[0]


def calculate_best_word(lst: list[dict[str, list[str]]]):
    CreateGeneralWordFrequency()

    frequency_of_word = {}
    most_common_word = ("", float('-inf'))
    total_length_of_dictionary_values = 0

    for dictionary in lst:
        for letter in dictionary:
            for word in dictionary[letter]:
                frequency_of_word.setdefault(word, 0)
                frequency_of_word[word] += len(dictionary[letter])
            total_length_of_dictionary_values += len(dictionary[letter])

    for word in frequency_of_word:

        repeated_letters = find_word_duplicate_letters(word)

        # curved_frequency_score = curve(
        #     frequency_of_word[word] / total_length_of_dictionary_values)
        #
        # score = curved_frequency_score * (1 - (
        #         len(repeated_letters) * 2 / len(word)))

        # if word == 'cross':
        #     print("cross")
        #
        score = frequency_of_word[word]

        score = frequency_of_word[word] * (1 - (
                len(repeated_letters) * 2.25 / len(word)))

        #
        # if word in generalWordFrequency:
        #     score *= generalWordFrequency[word]
        # else:
        #     score *= 0

        if score > most_common_word[1]:
            most_common_word = (word, score)

    return most_common_word[0]


def _test_best_word():
    portionedLetter = [words_letters_at_pos(0), words_letters_at_pos(1),
                       words_letters_at_pos(2), words_letters_at_pos(3),
                       words_letters_at_pos(4)]

    print("Recommended next word: ", calculate_best_word(
        portionedLetter))


def calculate_next_best_word(lst_of_dicts: list[dict[str, list[str]]],
                             list_of_remaining_words: list[str]) -> str:
    CreateGeneralWordFrequency()

    frequency_of_word = {}
    most_common_word = ("", 0)

    # total_length_of_dictionary_values = 0

    for dictionary in lst_of_dicts:
        for letter in dictionary:
            for word in dictionary[letter]:
                frequency_of_word.setdefault(word, 0)
                frequency_of_word[word] += len(dictionary[letter])
                # total_length_of_dictionary_values += len(dictionary[letter])

    for word in list_of_remaining_words:
        frequency_of_word.setdefault(word, 0)
        for dictionary in lst_of_dicts:
            for letter in dictionary:
                if word in dictionary[letter]:
                    frequency_of_word[word] += 2 * len(dictionary[letter])

    for word in frequency_of_word:

        repeated_letters = find_word_duplicate_letters(word)

        # curved_frequency_score = curve(
        #     frequency_of_word[word] / total_length_of_dictionary_values)
        #
        # score = curved_frequency_score * (1 - (
        #         len(repeated_letters) * 2 / len(word)))

        score = frequency_of_word[word] * (1 - (
                len(repeated_letters) * 2 / len(word)))

        if word in generalWordFrequency:
            score *= generalWordFrequency[word]
        else:
            score *= 0

        if score > most_common_word[1]:
            most_common_word = (word, score)

    return most_common_word[0]


def find_word_duplicate_letters(word: str) -> dict[str, list[tuple[int, int]]]:
    repeated_letters = {}

    _helper_word_contains_duplicate(word, repeated_letters)

    return repeated_letters


def _helper_word_contains_duplicate(word: str, repeated_letters):
    for i in range(len(word)):
        if ((word[i] in word[:i] or word[i] in word[i + 1:])
                and word[i] not in repeated_letters):
            repeated_letters[word[i]] = i
            _helper_word_contains_duplicate(word, repeated_letters)
            return
    return


def runAutomatedWordle(answer: str) -> int:
    portionedLetter = [words_letters_at_pos(0), words_letters_at_pos(1),
                       words_letters_at_pos(2), words_letters_at_pos(3),
                       words_letters_at_pos(4)]

    next_word_function = calculate_new_next_best_word

    guess = calculate_new_next_best_word(portionedLetter)

    guess = guess.strip().lower()

    # print(1, " " + guess)

    l5 = getGuessOutput(guess, answer, portionedLetter)

    num_guesses = 2

    while len(l5) > 1 and num_guesses <= 6:
        guess = next_word_function(portionedLetter)
        guess = guess.strip().lower()
        num_guesses += 1
        # print(num_guesses, " " + guess)
        l5 = getGuessOutput(guess, answer, portionedLetter)

    if len(l5) > 1:
        num_guesses = 7
        # print(l5, " " + answer)
    else:
        num_guesses -= 1

    # print(num_guesses, " " + l5[0])
    return num_guesses


def getGuessOutput(guess: str, answer: str,
                   list_of_dicts: list[dict[str, list[str]]]) -> list[
    dict[str, list[str]]]:
    repeated_letters = find_word_duplicate_letters(guess)
    repeated_letters_status = {}

    for i in range(len(list_of_dicts)):

        if guess[i] in answer:
            if guess[i] == answer[i]:
                letterStatus = '0'
            else:
                letterStatus = '1'
        else:
            letterStatus = '-1'

        if guess[i] in repeated_letters:
            repeated_letters_status.setdefault(guess[i], [])
            repeated_letters_status[guess[i]].append((i, letterStatus))

        if letterStatus == '0':
            list_of_dicts[i] = remove_all_but_one_key(list_of_dicts[i],
                                                      guess[i])

        elif letterStatus == '1':
            remove_key_from_dic(list_of_dicts[i], guess[i])

        elif letterStatus == '-1' and guess[i] not in repeated_letters:
            for j in range(len(list_of_dicts)):
                remove_key_from_dic(list_of_dicts[j], guess[i])

    _new_wordle_deal_with_duplicate_letters(list_of_dicts,
                                            repeated_letters_status)

    l5 = _update_list_of_dicts(list_of_dicts)

    return l5


def _runTrail(number_of_guesses):
    number_of_guesses.append(
        runAutomatedWordle(random.choice(five_letter_words)))


def joinThreads(threads: list[threading.Thread]):
    for thread in threads:
        thread.join()


def runTrails(n):
    global five_letter_words
    five_letter_word_maker()
    threads = []
    number_of_guesses = []
    for _ in range(min(n, 100)):
        threads.append(threading.Thread(target=_runTrail,
                                        args=(number_of_guesses,)))

        threads[-1].start()

    joinThreads(threads)
    i = len(threads)
    j = 0
    while i < n:
        threads[j] = threading.Thread(target=_runTrail,
                                      args=(number_of_guesses,))

        threads[j].start()
        i += 1
        j += 1

        if j >= len(threads):
            j = 0
            joinThreads(threads)

    plt.hist(number_of_guesses, range=(1, 8), bins=7, rwidth=0.5, align='left',
             color=(0, 0, 0))

    plt.title(f'Frequency of Guesses on random words.\n'
              f' (Doubles Penalty Multiplier of 2.25) n={n}')

    plt.xlabel("Number of Guesses to get answer")
    plt.ylabel("Frequency")
    plt.show()


# _test_best_word()

new_wordle()

# runTrails(100)

