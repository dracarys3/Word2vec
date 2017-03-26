#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Loreto Parisi <loretoparisi@gmail.com>
# Copyright (C) 2016 Silvio Ogliastri <silvio.olivastri@gmail.com>
# Licensed under the GNU LGPL v2.1 - http://www.gnu.org/licenses/lgpl.html

"""
USAGE: $ python -m gensim.scripts.word2vec2tensor --input <Word2Vec model file> --output <TSV tensor filename prefix>
Where:
    <Word2Vec model file>: Input Word2Vec model
    <TSV tensor filename prefix>: 2D tensor TSV output file name prefix
Output:
    The script will create two TSV files. A 2d tensor format file, and a Word Embedding metadata file. Both files will
    us the --output file name as prefix
This script is used to convert the word2vec format to Tensorflow 2D tensor and metadata formats for Embedding Visualization
For more information about TensorBoard format see: https://www.tensorflow.org/versions/master/how_tos/embedding_viz/
"""

import os
import sys
import random
import logging
import argparse

import gensim

logger = logging.getLogger(__name__)

'''
    Convert Word2Vec mode to 2D tensor TSV file and metadata file 
    @word2vec_model_path word2vec model
    @tensor_filename tensor filename prefix
'''
def word2vec2tensor(word2vec_model_path,tensor_filename):
    
    model = gensim.models.Word2Vec.load_word2vec_format(word2vec_model_path, binary=False)
    outfiletsv = tensor_filename + '_tensor.tsv'
    outfiletsvmeta = tensor_filename + '_metadata.tsv'
    
    with open(outfiletsv, 'w+') as file_vector:
        with open(outfiletsvmeta, 'w+') as file_metadata:
            for word in model.index2word:
                file_metadata.write(gensim.utils.to_unicode(word) + '\n')
                vector_row = '\t'.join(map(str, model[word]))
                file_vector.write(vector_row + '\n')

if __name__ == "__main__":
    logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s", ' '.join(sys.argv))

    # check and process cmdline input
    program = os.path.basename(sys.argv[0])
    if len(sys.argv) < 2:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", required=True,
        help="Input word2vec model")
    parser.add_argument(
        "-o", "--output", required=True,
        help="Output tensor file name prefix")
    args = parser.parse_args()

    word2vec2tensor(args.input, args.output)

    logger.info("finished running %s", program)
