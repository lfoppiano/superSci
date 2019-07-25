# This script postprocess text output from jats2text.py, but, in general, any text file
# Postprocessing rules:
#   - remove Fig. , Sec. and other reference markers that were not specified by XML tags
#       (can be finetuned by modifying the variable `remove_ref_prefix`)
#   - each paragraph is split in sentences (using SpaCy segmenter)
#   - remove all sentences with less than 3 space-separated tokens


## Usage:
#   python postprocess.py input_path [--output output_path] [--pattern _jats.xml]

# where --output and --pattern are optional:
# --input_pattern define the suffix to match the files to be processed (by default text files)
# --output specifies the output directory, the script will re-create the input tree structure.
#   If this parameter is omitted, the output willbe printed on stdout


import argparse
import os
import re
import sys
import time
from os.path import isfile, join, basename, dirname, relpath

import spacy

parser = argparse.ArgumentParser(description='Postprocess sentences. ')
parser.add_argument('input', metavar='input', type=str, help='Input directory path')
parser.add_argument('--output', dest='output', help='Output directory path')
parser.add_argument('--pattern', dest='input_pattern',
                    help='Pattern for file selection matching the end of the string (xml, java, test.java, etc.)')

args = parser.parse_args()

input_path = args.input
output_path_root = args.output
if args.input_pattern is not None:
    input_pattern = args.input_pattern
else:
    input_pattern = 'txt'

onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(input_path) for f in fn if
             f.lower().endswith(input_pattern) and isfile(join(dp, f))]

total_files = len(onlyfiles)

nlp = spacy.load("en_core_web_sm", disable=['ner', 'tagger'])


def split_in_sentences(text):
    doc = nlp(text)
    sents = []
    for sent in doc.sents:
        sents.append(str(sent))

    return sents


remove_ref_prefix = [r'Figs?\. ', r'Refs?\. ', r'Secs?\. ', r'Eqs?\. ', r'Tables?\. ', r'\([-– ,]*\)', r'\[[-– ,]*\]',
                     r'\(equation \)']

counter = 0
start = time.time()

for file in onlyfiles:
    name = basename(file)

    print("Processing " + name)

    with open(file, 'r') as f:
        postprocessedLines = []
        for line in f.readlines():
            text = line
            for r in remove_ref_prefix:
                text = re.sub(r, '', text)
                # text = text.replace(r, '')

            text = text.replace("()", "").strip()
            text = ' '.join(text.split())
            for sentence in split_in_sentences(text):
                tokens = sentence.split(' ')
                if len(tokens) > 3:
                    postprocessedLines.append(sentence)

        if output_path_root is not None:
            relative_path = relpath(input, input_path)

            output_filename = basename(input).replace('.txt', '.post.txt')
            output_path = os.path.join(output_path_root, dirname(relative_path))
            os.makedirs(output_path, exist_ok=True)

            output_file = os.path.join(output_path, output_filename)

            with open(join(output_path, name), 'w') as f_output:
                for output_line in postprocessedLines:
                    f_output.write(str(output_line))
                    f_output.write('\n')
        else:
            for output_line in postprocessedLines:
                print(output_line)
            print("\n")

    counter += 1
    if counter % 10 == 0:
        end = time.time()
        print("Progress ({}/{}) in ({} s): {}%".format(counter, total_files, (end - start),
                                                       (counter / total_files) * 100))
        print("\n")
        sys.stdout.flush()
        start = time.time()
