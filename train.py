from __future__ import print_function
from helper_functions.text_preprocessing import *
from helper_functions.generate_LDA import *

# To train the model, place training corpus in Medline format in home directory (inside PubMed_LDA folder). To
# run the topic model on your own data, change "hepatotoxicity.medline" to that of the corpus file name.

filename = "hepatotoxicity.medline"
model_id = "hepatotoxicity_full"

# pre-processing text
abstract_list = get_abstract_list(filename)
texts = process_texts(abstract_list)

# run model
parameters = {}
parameters["parameter_list"] = str(parameters)
parameters["model_id"] = model_id
parameters["transformation"] = None
parameters["update_every"] = 1
parameters["minimum_probability"] = 0.01
parameters["alpha"] = 'auto'
# the following parameters should be changed to optimize the model
parameters["num_topics"] = 5
parameters["chunksize"]= 1600
parameters["passes"] = 20
parameters["iterations"] = 2000

run_LDA(texts, parameters)

# display topics


