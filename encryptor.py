#!/usr/bin/python
import sys
import argparse
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

decode_parser.add_argument("--cipher", required=True, type=str, help="type of cipher")
decode_parser.add_argument("--key", required=True, type=str, help="cipher's key")
decode_parser.add_argument("--input-file", type=str, help="input file")
decode_parser.add_argument("--output-file", type=str, help="output file")

encode_parser.add_argument("--cipher", required=True, type=str, help="type of cipher")
encode_parser.add_argument("--key", required=True, type=str, help="cipher's key")
encode_parser.add_argument("--input-file", type=str, help="input file")
encode_parser.add_argument("--output-file", type=str, help="output file")

hack_parser.add_argument("--cipher", required=True, type=str, help="type of cipher")
hack_parser.add_argument("--key", required=True, type=str, help="cipher's key")
hack_parser.add_argument("--input-file", type=str, help="input file")
hack_parser.add_argument("--output-file   ", type=str, help="output file")

train_parser.add_argument("--text-file", type=str, help='training text file')
train_parser.add_argument("--model-file", required=True, type=str, help='path to model')


def normalize(i, n):
    i %= n
    if i < 0:
        i += n
    return i


def encode_vigenere_string(s, key):
    i = 0
    n = len(key)
    t = ''
    for symb in s:
        j = ord(symb) - ord('a')
        j = normalize(j + ord(key[i]) - ord('a'), 26)
        symb = chr(j + ord('a'))
        i = normalize(i + 1, n)
        t += symb
    return t


def decode_vigenere_string(s, key):
    i = 0
    n = len(key)
    t = ''
    for symb in s:
        j = ord(symb) - ord('a')
        j = normalize(j - ord(key[i]) + ord('a'), 26)
        symb = chr(j + ord('a'))
        i = normalize(i + 1, n)
        t += symb
    return t


def encode_caesar_string(s, key):
    word = chr(ord('a') + normalize(key, 26))
    return encode_vigenere_string(s, word)


def decode_caesar_string(s, key):
    return encode_caesar_string(s, -key)


args = parser.parse_args()

if args.module == 'encode':
    if args.cipher == 'caesar':
        string = ''
        if args.input_file is not None:
            with open(args.input_file, 'r') as f:
                string = f.read()
                f.close()
        else:
            string = input()
        key = int(args.key)
        result = encode_caesar_string(string, key)
        if args.output_file is not None:
            with open(args.output_file, 'w') as f:
                f.write(result)
                f.close()
        else:
            print(result)

    elif args.cipher == 'vigenere':
        string = ''
        if args.input_file is not None:
            with open(args.input_file, 'r') as f:
                string = f.read()
                f.close()
        else:
            string = input()
        key = args.key
        result = encode_vigenere_string(string, key)
        if args.output_file is not None:
            with open(args.output_file, 'w') as f:
                f.write(result)
                f.close()
        else:
            print(result)

elif args.module == 'decode':
    if args.cipher == 'caesar':
        string = ''
        if args.input_file is not None:
            with open(args.input_file, 'r') as f:
                string = f.read()
                f.close()
        else:
            string = input()
        key = int(args.key)
        result = decode_caesar_string(string, int(key))
        if args.output_file is not None:
            with open(args.output_file, 'w') as f:
                f.write(result)
                f.close()
        else:
            print(result)

    elif args.cipher == 'vigenere':
        string = ''
        if args.input_file is not None:
            with open(args.input_file, 'r') as f:
                string = f.read()
                f.close()
        else:
            string = input()
        key = args.key
        result = decode_vigenere_string(string, key)
        if args.output_file is not None:
            with open(args.output_file, 'w') as f:
                f.write(result)
                f.close()
        else:
            print(result)


