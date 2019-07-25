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
from os.path import isfile, join, basename

parser = argparse.ArgumentParser(description='Postprocess sentences. ')
parser.add_argument('input', metavar='input', type=str, help='Input directory path')
parser.add_argument('output', metavar='output', type=str, help='Output file')
parser.add_argument('--pattern', dest='input_pattern',
                    help='Pattern for file selection matching the end of the string (xml, java, test.java, etc.)')

args = parser.parse_args()

input_path = args.input
output_path = args.output
if args.input_pattern is not None:
    input_pattern = args.input_pattern
else:
    input_pattern = 'txt'

onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(input_path) for f in fn if
             f.lower().endswith(input_pattern) and isfile(join(dp, f))]

total_files = len(onlyfiles)

remove_ref_prefix = [r'Figs?\. ', r'Refs?\. ', r'Secs?\. ', r'Eqs?\. ', r'Tables?\. ', r'\([-– ,]*\)', r'\[[-– ,]*\]',
                     r'\(equation \)']

counter = 0
start = time.time()

with open(output_path, 'w') as f_output:
    for file in onlyfiles:
        name = basename(file)

        print("Processing " + name)
        with open(file, 'r') as f:
            postprocessedLines = []
            for line in f.readlines():
                text = line
                for r in remove_ref_prefix:
                    text = re.sub(r, '', text)

                text = ' '.join(text.split())
                postprocessedLines.append(text)

            file_as_line = ' '.join(postprocessedLines)
            f_output.write(str(file_as_line))
            f_output.write('\n')
            f_output.flush()

    counter += 1
    if counter % 10 == 0:
        end = time.time()
        print("Progress ({}/{}) in ({} s): {}%".format(counter, total_files, (end - start),
                                                       (counter / total_files) * 100))
        print("\n")
        sys.stdout.flush()
        start = time.time()