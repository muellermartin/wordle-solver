# Wordle solver

## Wordle
Wordle is a word guessing game similar to Hangman with elements from Mastermind.

There are several popular web based versions, for example:
- English: https://www.powerlanguage.co.uk/wordle/
- German: https://wordle.uber.space/

## Usage

```
python3 wordle-solver.py [DICTIONARY]
```

On start, wordle-solver.py will show the notation and list "good" candidates for a first guess. Good candidates include statistically more frequent letters and no repeated characters (this might change).

On each round the guessed word must be typed (case insensitive). After that, the result must be type (case sensitive!): Matching letters (often shown in green) must be typed in CAPITAL LETTERS, letters in the wrong position must be typed in small letters (often shown in yellow) and all non-matching letters (often shown in gray) must be replaced with an underscore (`_`).

### Result notation
```
LARGE LETTER: correct position (green)
small letter: wrong position (yellow)
Underscore:   not in word (grey)
```

## Dictionary

By default, `wordle-solver.py` uses the English [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) which is automatically downloaded, if not present in the current working directory.

A custom dictionary can be used by specifying a file as the first command line argument. All words in the dictionary file must be written in CAPITAL LETTERS and end with at least one space character (this might change).
