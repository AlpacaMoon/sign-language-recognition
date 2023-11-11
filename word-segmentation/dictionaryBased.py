import gzip
import os
import re
from math import log

class LanguageModel:
    def __init__(self, word_file):
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
        with gzip.open(word_file) as f:
            words = f.read().decode().split()
        # draw a dict that contains the words and the costs
        # Zipf's law = most common element occurs approximately twice as often as the second most common element, three times as often as the third most common element, and so on.
        # in this case, the probability is calculated using the position of word
        self._wordcost = {k: log((i + 1) * log(len(words))) for i, k in enumerate(words)}
        self._maxword = max(len(x) for x in words)
        print(self._wordcost)
        print(self._maxword)

    def split(self, s):
        # Uses dynamic programming to infer the location of spaces in a string without spaces.
        l = [self._split(x) for x in _SPLIT_RE.split(s)]
        print(l)
        return [item for sublist in l for item in sublist]

    def _split(self, s):
        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        def best_match(i):
            print(cost)
            # k is the position of candidates and c is the cost of candidate at k 
            candidates = enumerate(reversed(cost[max(0, i - self._maxword) : i]))
            return min((c + self._wordcost.get(s[i - k - 1 : i].lower(), 9e999), k + 1) for k, c in candidates)

        # Build the cost array.
        cost = [0]
        for i in range(1, len(s) + 1):
            c, k = best_match(i)
            print(c, k)
            cost.append(c)
        
        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i > 0:
            # c is cost k is the number of character
            # find the best cost
            c, k = best_match(i)
            print('best match')
            print(c, k)
            # trace back if c is in the list
            # assert c == cost[i]
            
            new_token = True
            # if not s[i - k : i] == "'":  # ignore a lone apostrophe
            #     if len(out) > 0:
            #         # re-attach split 's and split digits
            #         if out[-1] == "'s" or (s[i - 1].isdigit() and out[-1][0].isdigit()):  # digit followed by digit
            #             out[-1] = s[i - k : i] + out[-1]  # combine current token with the previous token
            #             new_token = False

            if new_token:
                out.append(s[i - k : i])

            i -= k

        return list(reversed(out))


def load_default_language_model():
    word_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictionary", "wordninja_words.txt.gz")
    return LanguageModel(word_file_path)


_SPLIT_RE = re.compile(r"[^a-zA-Z0-9']+")

def split_words(input_string):
    return DEFAULT_LANGUAGE_MODEL.split(input_string)


if __name__ == "__main__":
    DEFAULT_LANGUAGE_MODEL = load_default_language_model()
    input_string = "Mynameisadam"
    words = split_words(input_string)
    print(words)
