import nltk
nltk.download('punkt')
import re
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj NP VP | NP VP Conj VP

NP -> N | Det N | Det AP NP | P NP | NP P NP
VP -> V | VP NP | Adv VP | V Adv | VP NP | V NP Adv
AP -> Adj | AP Adj
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    lowercase_sentence = sentence.lower()
    sentence_words = nltk.tokenize.word_tokenize(lowercase_sentence)
    for word in sentence_words:
        if not re.search('[a-zA-Z]', word):
            sentence_words.remove(word)
    return sentence_words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    def check(subtree):
        if subtree.label() == "NP":
            return True
        # subtree has 1 child => terminal node => False unless label = s
        if len(subtree) == 1 and subtree.label() != 'S':
            return False
        for subsubtree in subtree:
            if isinstance(subsubtree, nltk.tree.Tree) and check(subsubtree):
                return True
        return False

    np_chunks = []

    for subtree in tree:
        if isinstance(subtree, nltk.tree.Tree):
            contains_np = check(subtree)
            if subtree.label() == "NP" and not contains_np:
                np_chunks.append(subtree)
            else:
                # recursively check for np cunks in the subtree
                np_chunks.extend(np_chunk(subtree))

    if tree.label() == "NP" and contains_np == False:
        np_chunks.append(tree)

    return np_chunks


if __name__ == "__main__":
    main()
