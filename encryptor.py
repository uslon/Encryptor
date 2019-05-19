#!/usr/bin/python3
import argparse
import pickle
import collections
import string
import sys

PARSER = argparse.ArgumentParser()
SUBS = PARSER.add_subparsers()
STAT = {}
POS = {}
ALPHABET = string.ascii_letters + string.digits + string.punctuation + '\n\t —”“'
LENGTH = len(ALPHABET)


def fill_standard_alphabet():
    cnt = 0
    for letter in ALPHABET:
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
    not_found = dict()
    for letter in string:
        if letter not in POS:
            not_found[letter] = 1
            continue
        j = POS[letter]
        j = normalize(j + POS[key[i]] * flag, LENGTH)

        letter = ALPHABET[j]
        i = normalize(i + 1, key_size)
        encoded_string += letter

    '''
    print("Symbols which are currently not in alphabet")
    for key in not_found:
        print(key)
    '''

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


def distance(dict_a, dict_b, flag):
    dist = 0
    for letter in dict_a.keys():
        dist += abs(dict_a[letter] - dict_b[letter])
        if flag:
            print(dict_a[letter], dict_b[letter], letter)
    return dist


def main():
    parse_args()
    args = PARSER.parse_args()
    fill_standard_alphabet()

    if args.module == 'encode':
        if args.cipher == 'caesar':
            string = ''
            if args.input_file is not None:
                with open(args.input_file, 'r') as f:
                    string = f.read()
            else:
                string = sys.stdin.read()

            KEY = int(args.key)
            result = encode_caesar_string(string, KEY)
            if args.output_file is not None:
                with open(args.output_file, 'w') as f:
                    f.write(result)
            else:
                print(result)

        elif args.cipher == 'vigenere':
            string = ''
            if args.input_file is not None:
                with open(args.input_file, 'r') as f:
                    string = f.read()
            else:
                string = sys.stdin.read()

            KEY = args.key
            check_key(KEY)
            result = encode_vigenere_string(string, KEY)
            if args.output_file is not None:
                with open(args.output_file, 'w') as f:
                    f.write(result)
            else:
                print(result)

    elif args.module == 'decode':
        if args.cipher == 'caesar':
            string = ''
            if args.input_file is not None:
                with open(args.input_file, 'r') as f:
                    string = f.read()
            else:
                string = sys.stdin.read()

            KEY = int(args.key)
            result = decode_caesar_string(string, int(KEY))
            if args.output_file is not None:
                with open(args.output_file, 'w') as f:
                    f.write(result)
            else:
                print(result)

        elif args.cipher == 'vigenere':
            string = ''
            if args.input_file is not None:
                with open(args.input_file, 'r') as f:
                    string = f.read()
            else:
                string = sys.stdin.read()

            KEY = args.key
            check_key(KEY)
            result = decode_vigenere_string(string, KEY)
            if args.output_file is not None:
                with open(args.output_file, 'w') as f:
                    f.write(result)
            else:
                print(result)

    elif args.module == 'train':
        init_standard_alphabet()
        training_string = ''
        if args.text_file is not None:
            with open(args.text_file, 'r') as f:
                training_string = f.read()
        else:
            training_string = sys.stdin.read()

        for symbol in training_string:
            if symbol not in STAT:
                continue
            STAT[symbol] += 1

        for symbol in STAT.keys():
            STAT[symbol] /= len(training_string)

        with open(args.model_file, "wb") as model:
            pickle.dump(STAT, model)
    else:
        init_standard_alphabet()
        hacking_string = ''
        if args.input_file is not None:
            with open(args.input_file, 'r') as f:
                hacking_string = f.read()
        else:
            hacking_string = sys.stdin.read()

        dic = {}
        with open(args.model_file, 'rb') as f:
            dic = pickle.load(f)

        rank = collections.Counter()
        for symbol in hacking_string:
            STAT[symbol] += 1

        for symbol in STAT.keys():
            STAT[symbol] /= len(hacking_string)

        last_key = None
        first_value = None
        for shift in range(LENGTH + 1):
            rank[shift] = distance(STAT, dic, False)
            for key, value in STAT.items():
                if first_value is None:
                    first_value = value
                else:
                    STAT[last_key] = value
                last_key = key
            STAT[last_key] = first_value

        key = rank.most_common()[-1][0]
        result = decode_caesar_string(hacking_string, key)

        '''
        for key, value in rank.items():
            print(key, value)
        '''

        if args.output_file is not None:
            with open(args.output_file, 'w') as f:
                f.write(result)
        else:
            print(result)


if __name__ == "__main__":
    main()
