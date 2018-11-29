#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import nltk
import string
import os
import readability

def convert_epub_to_text(epub_file_name):
    # TODO: yep, some other process could create a file between mktemp and
    # ebook-convert...
    txt_file_name = tempfile.mktemp(".txt")
    subprocess.run(["ebook-convert", epub_file_name, txt_file_name], stdout=subprocess.DEVNULL)
    return txt_file_name

def count_different_words(text):
    words = {}

    for word in text:
        if word in words:
            words[word] += 1
        else:
            words[word] = 1


    return len(words)

def word_study(epub_file_name):
    f = open(txt_file_name, "r")
    all_book = f.read()
    tokenized = nltk.tokenize.word_tokenize(all_book)
    table = str.maketrans('', '', string.punctuation)
    clean = [token.translate(table) for token in tokenized]

    for _ in range(clean.count("")):
        clean.remove("")

    clean = [word.lower() for word in clean]

    different_word_count = count_different_words(clean)
    total_count = len(clean)
    print("Different words:", different_word_count)
    print("Total number of words:", total_count)
    print("New word every: {:.2f}".format(total_count/different_word_count))
    print()

    return{"different_words": different_word_count,
           "total_number_words": total_count,
           "new_word_every": total_count/different_word_count}

def readability_study(txt_file_name):
    f = open(txt_file_name, "r")

    text = f.read()

    measures = readability.getmeasures(text, lang="en")

    for cat, data in measures.items():
        print('%s:' % cat)
        for key, val in data.items():
            print(('    %-25s %12.2f' % (key + ':', val)
                   ).rstrip('0 ').rstrip('.'))

    return measures

if __name__ == "__main__":
    epub_file_name = sys.argv[1]
    epub_base_name = os.path.basename(epub_file_name)

    print(epub_base_name)
    print("="*len(epub_base_name))

    txt_file_name = convert_epub_to_text(epub_file_name)
    word_result = word_study(txt_file_name)
    readability_mesures = readability_study(txt_file_name)

    complex_words_dc = readability_mesures["sentence info"]["complex_words_dc"]
    print("% complex word:", (complex_words_dc / word_result["total_number_words"]) * 100)

    os.unlink(txt_file_name)
