#!/usr/bin/python
import argparse
import pickle
import collections
import string
import sys

PARSER = argparse.ArgumentParser()
SUBS = PARSER.add_subparsers()
ALPHABET = []
STAT = {}
POS = {}
LENGTH = len(string.ascii_letters) + len(string.digits) + len(string.punctuation)


def fill_standard_alphabet():
    cnt = 0
    for letter in string.ascii_letters:
        POS[letter] = cnt
        cnt += 1
        ALPHABET.append(letter)

    for digit in string.digits:
        POS[digit] = cnt
        cnt += 1
        ALPHABET.append(digit)

    for letter in string.punctuation:
        ALPHABET.append(letter)
        POS[letter] = cnt
        cnt += 1


def init_standard_alphabet():
    for i in ALPHABET:
        STAT[i] = 0


def parse_args():
    DECODE_PARSER = SUBS.add_parser("decode", description='this is decoding module')
    ENCODE_PARSER = SUBS.add_parser("encode", description='this is encoding module')
    HACK_PARSER = SUBS.add_parser("hack", description='this is hacking module')
    TRAIN_PARSER = SUBS.add_parser("train", description='this is training module')

    DECODE_PARSER.set_defaults(module="decode")
    ENCODE_PARSER.set_defaults(module="encode")
    HACK_PARSER.set_defaults(module="hack")
    TRAIN_PARSER.set_defaults(module="train")

    DECODE_PARSER.add_argument("--cipher", required=True, type=str, help="type of cipher")
    DECODE_PARSER.add_argument("--key", required=True, type=str, help="cipher's key")
    DECODE_PARSER.add_argument("--input-file", type=str, help="input file")
    DECODE_PARSER.add_argument("--output-file", type=str, help="output file")

    ENCODE_PARSER.add_argument("--cipher", required=True, type=str, help="type of cipher")
    ENCODE_PARSER.add_argument("--key", required=True, type=str, help="cipher's key")
    ENCODE_PARSER.add_argument("--input-file", type=str, help="input file")
    ENCODE_PARSER.add_argument("--output-file", type=str, help="output file")

    HACK_PARSER.add_argument("--input-file", type=str, help="input file")
    HACK_PARSER.add_argument("--output-file", type=str, help="output file")
    HACK_PARSER.add_argument("--model-file", required=True, type=str, help='path to model')

    TRAIN_PARSER.add_argument("--text-file", type=str, help='training text file')
    TRAIN_PARSER.add_argument("--model-file", required=True, type=str, help='path to model')


def normalize(number, module):
    number %= module
    if number < 0:
        number += module
    return number


def encode_vigenere_string(string, key, flag=1):
    i = 0
    key_size = len(key)
    encoded_string = ''
    for letter in string:
        if letter not in POS:
            continue
        j = POS[letter]
        j = normalize(j + POS[key[i]] * flag, LENGTH)

        letter = ALPHABET[j]
        i = normalize(i + 1, key_size)
        encoded_string += letter
    return encoded_string


def decode_vigenere_string(string, key):
    return encode_vigenere_string(string, key, -1)


def encode_caesar_string(string, key):
    word = ALPHABET[normalize(key, LENGTH)]
    return encode_vigenere_string(string, word)


def decode_caesar_string(string, key):
    return encode_caesar_string(string, -key)


def check_key(key):
    for i in key:
        if i not in POS:
            raise KeyError("invalid key")


def distance(string_a, string_b):
    dist = 0
    for i in string_a.keys():
        dist += abs(string_a[i] - string_b[i])
    return dist


def main():
    parse_args()
    ARGS = PARSER.parse_args()
    fill_standard_alphabet()

    if ARGS.module == 'encode':
        if ARGS.cipher == 'caesar':
            STRING = ''
            if ARGS.input_file is not None:
                with open(ARGS.input_file, 'r') as f:
                    STRING = f.read()
            else:
                STRING = sys.stdin.read()

            KEY = int(ARGS.key)
            RESULT = encode_caesar_string(STRING, KEY)
            if ARGS.output_file is not None:
                with open(ARGS.output_file, 'w') as f:
                    f.write(RESULT)
            else:
                print(RESULT)

        elif ARGS.cipher == 'vigenere':
            STRING = ''
            if ARGS.input_file is not None:
                with open(ARGS.input_file, 'r') as f:
                    STRING = f.read()
            else:
                STRING = sys.stdin.read()

            KEY = ARGS.key
            check_key(KEY)
            RESULT = encode_vigenere_string(STRING, KEY)
            if ARGS.output_file is not None:
                with open(ARGS.output_file, 'w') as f:
                    f.write(RESULT)
            else:
                print(RESULT)

    elif ARGS.module == 'decode':
        if ARGS.cipher == 'caesar':
            STRING = ''
            if ARGS.input_file is not None:
                with open(ARGS.input_file, 'r') as f:
                    STRING = f.read()
            else:
                STRING = sys.stdin.read()

            KEY = int(ARGS.key)
            RESULT = decode_caesar_string(STRING, int(KEY))
            if ARGS.output_file is not None:
                with open(ARGS.output_file, 'w') as f:
                    f.write(RESULT)
            else:
                print(RESULT)

        elif ARGS.cipher == 'vigenere':
            STRING = ''
            if ARGS.input_file is not None:
                with open(ARGS.input_file, 'r') as f:
                    STRING = f.read()
            else:
                STRING = sys.stdin.read()

            KEY = ARGS.key
            check_key(KEY)
            RESULT = decode_vigenere_string(STRING, KEY)
            if ARGS.output_file is not None:
                with open(ARGS.output_file, 'w') as f:
                    f.write(RESULT)
            else:
                print(RESULT)

    elif ARGS.module == 'train':
        init_standard_alphabet()
        TRAINING_STRING = ''
        if ARGS.text_file is not None:
            with open(ARGS.text_file, 'r') as f:
                TRAINING_STRING = f.read()
        else:
            TRAINING_STRING = sys.stdin.read()

        for symbol in TRAINING_STRING:
            if symbol not in STAT:
                continue
            STAT[symbol] += 1

        with open(ARGS.model_file, "wb") as model:
            pickle.dump(STAT, model)
    else:
        init_standard_alphabet()
        STRING = ''
        if ARGS.input_file is not None:
            with open(ARGS.input_file, 'r') as f:
                STRING = f.read()
        else:
            STRING = sys.stdin.read()

        DIC = {}
        with open(ARGS.model_file, 'rb') as f:
            DIC = pickle.load(f)

        RANK = collections.Counter()
        for shift in range(LENGTH):
            decoded_string = decode_caesar_string(STRING, shift)
            for symbol in decoded_string:
                STAT[symbol] += 1
            RANK[shift] = distance(STAT, DIC)

        for shift in RANK.most_common()[-2:]:
            KEY = shift[0]
            print(shift)
            RESULT = decode_caesar_string(STRING, KEY)
            print("----------------------", KEY, "----------------------")
            if ARGS.output_file is not None:
                with open(ARGS.output_file, 'w') as f:
                    f.write(RESULT)
            else:
                print(RESULT)


if __name__ == "__main__":
    main()
