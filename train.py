from __future__ import print_function

# To train the model, place training corpus in Medline format in home directory (inside PubMed_LDA folder). Change
# "FILENAME.TXT" to that of the corpus file.

corpus_filename = "FILENAME.txt"

# pre-processing text

# convert corpus to document per line, extract text, then train 