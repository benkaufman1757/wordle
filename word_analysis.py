from collections import Counter

with open('dictionary.txt', 'r') as fp:
    dictionary = fp.readlines()

print(f'Number of words in dictionary {len(dictionary)}')

five_letter_words = [word.lower() for word in dictionary if len(word) == 5]

print(f'Number of 5-letter words in dictionary {len(five_letter_words)}')

print('5-letter word frequency distribution')
character_freq_dist = Counter(''.join(five_letter_words))
for char, count in character_freq_dist.most_common(10):
    if char.strip():
        print(char, count)
