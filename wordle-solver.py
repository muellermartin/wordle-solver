#!/usr/bin/env python3

import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request


DICTIONARY_URL = 'http://svn.code.sf.net/p/cmusphinx/code/trunk/cmudict/cmudict-0.7b'
DEBUG = False


def usage():
    text = '''\
Result notation:
\tLARGE LETTER:\tcorrect position (green)
\tsmall letter:\twrong position (yellow)
\tUnderscore:\tnot in word (grey)'''

    return text


def download_dictionary(url):
    url_parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(url_parsed.path)

    if pathlib.Path(filename).exists():
        return filename

    # TODO: Check HTTP status code
    urllib.request.urlretrieve(url, filename=filename)

    return filename


def load_dictionary(dictionary_path):
    dictionary = []

    if not pathlib.Path(dictionary_path).exists():
        print(f'Error: Dictionary file "{dictionary_path}" does not exist', file=sys.stderr)
        return None

    with open(dictionary_path, 'rb') as f:
        for line in f.readlines():
            try:
                word = line.decode()
                if re.match(r'^[A-Z]{5} ', word):
                    dictionary.append(word[:5])
            except UnicodeDecodeError:
                pass

    return dictionary


def ask_guess_and_result():
    while True:
        guess = input('Guess: ')

        if len(guess) != 5:
            print('Guess must have 5 charactes', file=sys.stderr)
            continue
        else:
            break

    while True:
        result = input('Result: ')

        if len(result) != 5:
            print('Result must have 5 charactes', file=sys.stderr)
            continue
        elif not all([True if c[0].upper() == c[1].upper() or c[1] == '_' else False for c in zip(guess, result)]):
            # Check if result notation is valid
            print('Result notation is invalid')
            continue
        else:
            break

    return guess, result


def first_candidates(dictionary):
    # Choose words with three most common consonants
    # https://en.wikipedia.org/wiki/Letter_frequency
    candidates = [word for word in dictionary if 'E' in word and 'A' in word and 'I' in word and len(set(list(word))) == 5]

    return candidates


def clues_from_tries(dictionary, tries):
    exclude_letters = []
    include_letters = []
    exclude_positions = { 0: set(), 1: set(), 2: set(), 3: set(), 4: set() }
    include_positions = { 0: set(), 1: set(), 2: set(), 3: set(), 4: set() }
    candidates = []

    for guess, result in tries.items():
        for i, c in enumerate(zip(guess.upper(), result)):
            if c[1] == c[0].lower():
                include_letters.append(c[0])
                exclude_positions[i].add(c[0].upper())
            elif c[1] == c[0]:
                include_letters.append(c[0])
                include_positions[i].add(c[0])
            elif c[1] == '_' and c[0] not in include_letters:
                exclude_letters.append(c[0])

    if DEBUG:
        print(exclude_letters)
        print(include_letters)
        print(exclude_positions)
        print(include_positions)

    for word in dictionary:
        if any([c in word for c in exclude_letters]):
            # Skip word if any excluded letter is in word
            continue

        if not all([c in word for c in include_letters]):
            # Skip word if not all include letters are included
            continue

        if any([word[i] in excludes for i, excludes in exclude_positions.items()]):
            # Skip if any letter is in wrong position
            continue

        if not all([word[i] in includes for i, includes in include_positions.items() if includes != set()]):
            # Skip if any letter is in wrong position
            continue

        candidates.append(word)

    return candidates


def main():
    dictionary_path = download_dictionary(DICTIONARY_URL)
    dictionary = load_dictionary(dictionary_path)
    wordle_tries = {}

    print(usage())
    print('Candidates:', first_candidates(dictionary))

    for _ in range(6):
        guess, result = ask_guess_and_result()
        wordle_tries[guess] = result
        candidates = clues_from_tries(dictionary, wordle_tries)

        print('Candidates:', candidates)

        if len(candidates) <= 1:
            break


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print()
