
def get_all_possible_words(guess, output, dictionary):
    possible_words = dictionary.copy()
    for index, (g_char, o_char) in enumerate(zip(guess, output)):
        if o_char == 'A':
            possible_words = [word for word in possible_words if word[index] == g_char]
        if o_char == 'B':
            possible_words = [word for word in possible_words if word[index] != g_char and g_char in word]
        if o_char == 'C':
            possible_words = [word for word in possible_words if g_char not in word]

    return possible_words

def main():
    with open('dictionary.txt', 'r') as fp:
        dictionary = fp.readlines()

    five_letter_words = [word.lower().strip() for word in dictionary if len(word.strip()) == 5]
    word = 'query'

    assert word in five_letter_words

    while True:
        guess = input('Enter your guess: ')
        if len(guess) != 5:
            raise Exception('Guess must be a 5 letter word')

        output = ''
        for g_char, w_char in zip(guess, word):
            if g_char == w_char:
                output += 'A'
            elif g_char in word:
                output += 'B'
            else:
                output += 'C'
        print(output)
        if output == 'AAAAA':
            print(f'You Won! The Word was: {word}')
            break

if __name__ == '__main__':
    main()

# if you want to see the word
# Inspect -> Application -> Local Storage -> Game State -> Solution