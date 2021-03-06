#!/usr/bin/python3
import argparse
import pickle
import collections
import string
import sys

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
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers()

    decode_parser = subs.add_parser("decode", description='this is decoding module')
    encode_parser = subs.add_parser("encode", description='this is encoding module')
    hack_parser = subs.add_parser("hack", description='this is hacking module')
    train_parser = subs.add_parser("train", description='this is training module')

    decode_parser.set_defaults(module="decode")
    encode_parser.set_defaults(module="encode")
    hack_parser.set_defaults(module="hack")
    train_parser.set_defaults(module="train")

    decode_parser.add_argument("--cipher", required=True, type=str, help="type of cipher", choices=['caesar', 'vigenere'])
    decode_parser.add_argument("--key", required=True, type=str, help="cipher's key")
    decode_parser.add_argument("--input-file", type=str, help="input file")
    decode_parser.add_argument("--output-file", type=str, help="output file")

    encode_parser.add_argument("--cipher", required=True, type=str, help="type of cipher", choices=['caesar', 'vigenere'])
    encode_parser.add_argument("--key", required=True, type=str, help="cipher's key")
    encode_parser.add_argument("--input-file", type=str, help="input file")
    encode_parser.add_argument("--output-file", type=str, help="output file")

    hack_parser.add_argument("--input-file", type=str, help="input file")
    hack_parser.add_argument("--output-file", type=str, help="output file")
    hack_parser.add_argument("--model-file", required=True, type=str, help='path to model')

    train_parser.add_argument("--text-file", type=str, help='training text file')
    train_parser.add_argument("--model-file", required=True, type=str, help='path to model')

    return parser

def normalize(number, module):
    number %= module
    if number < 0:
        number += module
    return number


def encode_vigenere_string(encoding_string, key, flag=1):
    i = 0
    key_size = len(key)
    not_found = dict()
    encoded_string = ''
    letters = []
    for letter in encoding_string:
        if letter not in POS:
            not_found[letter] = 1
            continue
        j = POS[letter]
        j = normalize(j + POS[key[i]] * flag, LENGTH)

        letter = ALPHABET[j]
        i = normalize(i + 1, key_size)
        letters.append(letter)
    encoded_string = "".join(letters)

    return encoded_string


def decode_vigenere_string(decoding_string, key):
    return encode_vigenere_string(decoding_string, key, -1)


def encode_caesar_string(encoding_string, key):
    word = ALPHABET[normalize(key, LENGTH)]
    return encode_vigenere_string(encoding_string, word)


def decode_caesar_string(decoding_string, key):
    return encode_caesar_string(decoding_string, -key)


def check_key(key):
    for i in key:
        if i not in POS:
            raise RuntimeError("Invalid key")


def distance(dict_a, dict_b, flag):
    dist = 0
    for letter in dict_a.keys():
        dist += abs(dict_a[letter] - dict_b[letter])
        if flag:
            print(dict_a[letter], dict_b[letter], letter)
    return dist


def encode(args):
    if args.cipher == 'caesar':
        if args.input_file is not None:
            with open(args.input_file, 'r') as input_file:
                encoding_string = input_file.read()
        else:
            encoding_string = sys.stdin.read()

        key = int(args.key)
        result = encode_caesar_string(encoding_string, key)
        if args.output_file is not None:
            with open(args.output_file, 'w') as input_file:
                input_file.write(result)
        else:
            print()
            print(result)

    elif args.cipher == 'vigenere':
        if args.input_file is not None:
            with open(args.input_file, 'r') as input_file:
                encoding_string = input_file.read()
        else:
            encoding_string = sys.stdin.read()

        key = args.key
        check_key(key)
        result = encode_vigenere_string(encoding_string, key)
        if args.output_file is not None:
            with open(args.output_file, 'w') as input_file:
                input_file.write(result)
        else:
            print()
            print(result)


def decode(args):
    if args.cipher == 'caesar':
        if args.input_file is not None:
            with open(args.input_file, 'r') as input_file:
                decoding_string = input_file.read()
        else:
            decoding_string = sys.stdin.read()

        key = int(args.key)
        result = decode_caesar_string(decoding_string, int(key))
        if args.output_file is not None:
            with open(args.output_file, 'w') as input_file:
                input_file.write(result)
        else:
            print()
            print(result)

    elif args.cipher == 'vigenere':
        if args.input_file is not None:
            with open(args.input_file, 'r') as input_file:
                decoding_string = input_file.read()
        else:
            decoding_string = sys.stdin.read()

        key = args.key
        check_key(key)
        result = decode_vigenere_string(decoding_string, key)
        if args.output_file is not None:
            with open(args.output_file, 'w') as input_file:
                input_file.write(result)
        else:
            print()
            print(result)


def train(args):
    init_standard_alphabet()
    if args.text_file is not None:
        with open(args.text_file, 'r') as input_file:
            training_string = input_file.read()
    else:
        training_string = sys.stdin.read()

    for symbol in training_string:
        if symbol not in STAT:
            continue
        STAT[symbol] += 1

    for symbol in STAT:
        STAT[symbol] /= len(training_string)

    with open(args.model_file, "wb") as model:
        pickle.dump(STAT, model)


def hack(args):
    init_standard_alphabet()
    if args.input_file is not None:
        with open(args.input_file, 'r') as input_file:
            hacking_string = input_file.read()
    else:
        hacking_string = sys.stdin.read()

    with open(args.model_file, 'rb') as model_file:
        dic = pickle.load(model_file)

    rank = collections.Counter()
    for symbol in hacking_string:
        STAT[symbol] += 1

    for symbol in STAT:
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
    if args.output_file is not None:
        with open(args.output_file, 'w') as input_file:
            input_file.write(result)
    else:
        print()
        print(result)


def main():
    parser = parse_args()
    args = parser.parse_args()
    fill_standard_alphabet()

    if args.module == 'encode':
        encode(args)
    elif args.module == 'decode':
        decode(args)
    elif args.module == 'train':
        train(args)
    else:
        hack(args)


if __name__ == "__main__":
    main()
