# This script process JATS XML file and extract text as paragraphs.

# It extracts paragraphs (namely everything within <p>), excluding
# formulas, inline-formulas, references and other useless information.
# There is minimal post-processing part, where all additional breadlines are removed

# If the --output is specified the files are written keeping the input directory stucture

## Usage:
#   python jats2text.py input_path [--output output_path] [--input_pattern _jats.xml]

# where --output and --input_pattern are optional
# --input_pattern define the suffix to match the files to be processed
# (when not specified it's assuming all files ending with xml)

import argparse
import os
import sys
import time
from os import makedirs
from os.path import isfile, join, relpath, basename, dirname

from bs4 import BeautifulSoup


def remove_tags(soup, tag):
    for nodes in soup.find_all(tag):
        nodes.extract()

    return soup


parser = argparse.ArgumentParser(description='Extract texts as sentences from JATS XML format of scientific articles. ')
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
    input_pattern = 'xml'

file_list = [os.path.join(dp, f) for dp, dn, fn in os.walk(input_path) for f in fn if
             f.lower().endswith(input_pattern) and isfile(join(dp, f))]

# input = open('/Users/lfoppiano/development/superconductors/supercon_papers/aip/072502_1/vor_1.5033353.xml')
# input = open('/Users/lfoppiano/development/projects/embeddings/tmp/10.1063_1.4985098_jats.xml')

total_files = len(file_list)
print("Processing " + str(total_files) + " files. ")

counter = 0

# Remove tags
ignored_tag = ['xref', 'disp-formula', 'inline-formula', 'ext-link', 'label']
ignored_parents = ['author-comment']

start = time.time()
for file in file_list:

    with open(file, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')

        soup = remove_tags(soup, ignored_tag)

        paragraphs = []
        # Collect and strip paragraphs and remove additional breaklines
        for paragraph in soup.find_all('p'):
            if paragraph.parent.name not in ignored_parents:
                text = paragraph.text.strip()
                paragraphs.append(' '.join(text.split()))

        # Output
        if output_path_root is not None:
            # common_path = commonpath([input_path, output_path])
            relative_path = relpath(file, input_path)

            output_filename = basename(file).replace('.xml', '.txt')
            output_path = os.path.join(output_path_root, dirname(relative_path))
            makedirs(output_path, exist_ok=True)

            output_file = os.path.join(output_path, output_filename)

            with open(output_file, 'w') as f_output:
                for paragraph in paragraphs:
                    f_output.write(str(paragraph))
                    f_output.write('\n')

        else:
            print(file + "\n")
            for paragraph in paragraphs:
                print(paragraph)
            print("\n")

    counter += 1
    if counter % 10000 == 0:
        end = time.time()
        print("Progress ({}/{}) in ({} s): {}%".format(counter, total_files, (end - start),
                                                       (counter / total_files) * 100))
        sys.stdout.flush()
        start = time.time()

