# This script process JATS XML file and extract text as sentences.
# It extracts every paragraphs (namely everything within <p>) and it excludes formulas, inlinde formulas and references
# There is a small post-processing part, where all additional breaklines are removed.
# After sentence split, all sentences with less than 2 tokens (split by space) are removed.
# It uses Spacy segmenter for English to split paragraphs in sentences.

## Usage:
#   python jats2text.py input_path [--output output_path] [--input_pattern _jats.xml]

# where --output and --input_pattern are optional
# --input_pattern define the suffix to match the files to be processed
# (when not specified it's assuming all files ending with xml)

import argparse
import os
from os import makedirs
from os.path import isfile, join, relpath, basename, dirname

import spacy
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_sm", disable=['ner', 'tagger'])


def split_in_sentences(text):
    doc = nlp(text)
    sents = []
    for sent in doc.sents:
        sents.append(str(sent))

    return sents


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

onlyfiles = [os.path.join(dp, f) for dp, dn, fn in os.walk(input_path) for f in fn if
             f.lower().endswith(input_pattern) and isfile(join(dp, f))]

# input = open('/Users/lfoppiano/development/superconductors/supercon_papers/aip/072502_1/vor_1.5033353.xml')
# input = open('/Users/lfoppiano/development/projects/embeddings/tmp/10.1063_1.4985098_jats.xml')

print("Processing " + str(len(onlyfiles)))

for input in onlyfiles:

    with open(input, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')

        # Remove tags
        ignored_tag = ['xref', 'disp-formula', 'inline-formula']

        soup = remove_tags(soup, ignored_tag)

        datas = []
        # Collect
        for paragraphs in soup.find_all('p'):
            text = paragraphs.text.strip()
            datas.append(text)

        # Post-process
        remove_ref_prefix = ['Figs. ', 'Fig. ', 'Ref. ', 'Refs. ', 'Sec. ', 'Secs. ', 'Eq. ', 'Eqs. ']

        sentences = []
        for text in datas:
            for r in remove_ref_prefix:
                text = text.replace(r, '')

            text = text.replace("()", "").strip()
            # text = text.replace("\n", "")
            text = ' '.join(text.split())

            for s in split_in_sentences(text):
                if len(s.split(" ")) > 1:
                    sentences.append(s)

        # Output
        if output_path_root is not None:
            # common_path = commonpath([input_path, output_path])
            relative_path = relpath(input, input_path)

            output_filename = basename(input).replace('.xml', '.txt')
            output_path = os.path.join(output_path_root, dirname(relative_path))
            makedirs(output_path)

            output_file = os.path.join(output_path, output_filename)

            with open(output_file, 'w') as f_output:
                for sentence in sentences:
                    f_output.write(str(sentence))
                    f_output.write('\n')

        else:
            print(input + "\n")
            for sentence in sentences:
                print(sentence)
