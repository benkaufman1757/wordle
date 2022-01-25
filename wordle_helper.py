'''Quick and greedy wordle solver'''
from collections import Counter, defaultdict
import json
import random
import time

def get_words():
    '''load the words from a dictionary'''
    with open('dictionary.txt', 'r') as dict_file:
        dictionary = dict_file.readlines()

    return [word.lower().strip() for word in dictionary if len(word.strip()) == 5]

def score_guess(guess, word):
    '''Given a guess and the actual word score the guess'''
    output = ''
    for g_char, w_char in zip(guess, word):
        if g_char == w_char:
            output += 'A'
        elif g_char in word:
            output += 'B'
        else:
            output += 'C'
    return output

def get_all_possible_words(guess, output, dictionary):
    '''Given a guess and the output return all the possible words it could be'''
    possible_words = dictionary.copy()
    for index, (g_char, o_char) in enumerate(zip(guess, output)):
        if o_char == 'A':
            possible_words = [word for word in possible_words if word[index] == g_char]
        if o_char == 'B':
            possible_words = [word for word in possible_words if \
                word[index] != g_char and g_char in word]
        if o_char == 'C':
            possible_words = [word for word in possible_words if g_char not in word]

    return set(possible_words)

def get_next_guess(possibilities, agg=sum):
    '''
        Given a list of possible words find a guess that gives you
        the minimum number of future possibilities. You can change
        the aggregation function, agg, to use a mean function.
    '''
    if len(possibilities) < 2:
        return list(possibilities)[0]
    word_table = defaultdict(list)
    for possibility in possibilities:
        # pretend possibility is the new word
        sub_guesses = possibilities - set([possibility])
        for sub_guess in sub_guesses:
            sub_output = score_guess(sub_guess, possibility)
            sub_possibilities = get_all_possible_words(sub_guess, sub_output, sub_guesses)
            word_table[sub_guess].append(len(sub_possibilities))

    return min(word_table,key=lambda x: agg(word_table[x]))

def help_me():
    '''Main helping loop'''
    five_letter_words = get_words()
    possibilities = five_letter_words.copy()
    while True:
        guess = input('Enter your guess: ')
        if len(guess) != 5:
            raise Exception('Guess must be a 5 letter word')

        print(guess)
        output = input('Enter your previous guess\' response (Green->A, Yellow->B, Gray->C): ')

        possibilities = get_all_possible_words(guess, output, possibilities)
        print(f'Number of possible words: {len(possibilities)}')
        if len(possibilities) <= 20:
            print('All possible remaining words')
            for possibility in sorted(possibilities):
                print(possibility)
            print('=========')

        print(f'You should guess: {get_next_guess(possibilities)}')

def analyze(initial_guess='aeoli', verbose=True, save=True):
    '''Kowalski'''
    five_letter_words = get_words()

    data = {}
    start_time = time.time()
    for word in five_letter_words:
        possibilities = set(five_letter_words.copy())
        n_turns = 0
        while True:
            n_turns += 1

            if n_turns == 1 and initial_guess:
                guess = initial_guess
            else:
                guess = get_next_guess(possibilities)

            output = score_guess(guess, word)

            if output == 'AAAAA':
                break

            possibilities = get_all_possible_words(guess, output, possibilities)

        data[word] = n_turns
        if verbose:
            print(f'Solved {word} starting with {initial_guess} in {n_turns} turns')

    print(f'Solved all Wordles in {time.time()-start_time} seconds')

    if save:
        with open(f'wordle_solution_steps_initial_guess_{initial_guess}.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    for n_turns, count in Counter(data.values()).most_common():
        print(f'Number of wordles solve in {n_turns} turns: {count}')

def super_solve(word):
    '''For when you really wanna solve 1 in under 5 guesses'''
    five_letter_words = get_words()

    while True:
        initial_guess = random.choice(five_letter_words)
        possibilities = set(five_letter_words.copy())
        n_turns = 0
        while True:
            n_turns += 1
            if n_turns == 1:
                guess = initial_guess
            else:
                guess = get_next_guess(possibilities)

            output = score_guess(guess, word)

            if output == 'AAAAA':
                break

            possibilities = get_all_possible_words(guess, output, possibilities)
        if n_turns < 7:
            print(f'Solved {word} starting with {initial_guess} in {n_turns} turns')
            return
        else:
            print(f'Failed to solve {word} starting with {initial_guess} in 6 turns. Used {n_turns} turns')

if __name__ == '__main__':
    help_me()
    # analyze()
    # super_solve('mater')

# import json
# import operator

# with open('wordle_solution_steps_initial_guess_aeoli.json', 'r') as json_file:
#     data = json.load(json_file)

# for k, v in sorted(data.items(), key=operator.itemgetter(1),reverse=True):
#     if v > 6:
#         print(k, v)

# Solved all Wordles in 3086.70463013649 seconds
# Number of wordles solve in 4 turns: 1488
# Number of wordles solve in 3 turns: 1073
# Number of wordles solve in 5 turns: 438
# Number of wordles solve in 2 turns: 106
# Number of wordles solve in 6 turns: 76
# Number of wordles solve in 7 turns: 19
# Number of wordles solve in 8 turns: 7
# Number of wordles solve in 9 turns: 2
# Number of wordles solve in 10 turns: 1

# mater 10
# dater 9
# jerry 9
# barry 8
# dolly 8
# ferry 8
# found 8
# hatch 8
# hater 8
# hitch 8
# bater 7
# blade 7
# bronx 7
# drown 7
# folly 7
# froze 7
# furze 7
# gusty 7
# marry 7
# match 7
# perry 7
# pitch 7
# plasm 7
# pride 7
# rilly 7
# shape 7
# sound 7
# swore 7
# taste 7


