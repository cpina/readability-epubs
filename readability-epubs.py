#!/usr/bin/env python3

import sys
import subprocess
import tempfile
import nltk
import string
import os

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

def process_filename(epub_file_name):
    txt_file_name = convert_epub_to_text(epub_file_name)
    f = open(txt_file_name)
    all_book = f.read()
    tokenized = nltk.tokenize.word_tokenize(all_book)
    table = str.maketrans('', '', string.punctuation)
    clean = [token.translate(table) for token in tokenized]

    for _ in range(clean.count("")):
        clean.remove("")

    clean = [word.lower() for word in clean]

    different_word_count = count_different_words(clean)
    total_count = len(clean)
    file_base_name = os.path.basename(epub_file_name)

    print(file_base_name)
    print("="*len(file_base_name))
    print("Different words:", different_word_count)
    print("Total number of words:", total_count)
    print("New word every: {:.2f}".format(total_count/different_word_count))

    os.unlink(txt_file_name)

if __name__ == "__main__":
    file_name = sys.argv[1]
    process_filename(file_name)