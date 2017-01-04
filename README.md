# PubMed_LDA
Creating topic model based on corpus of PubMed documents related to hepatotoxicity. Topic model uses Latent Dirichlet Allocation. 
The script is written in Python 2.7 and requires installation of the following packages: anaconda, gensim, matplotlib, wordcloud, NLTK

In order to create the model, first run train.py. This will create the LDA model based on either the default parameters or the ones you specify. The generated model will then be pickled and available for use by the other two scripts. display_topics.py will generate wordcloud images topics within the model and classify_documents.py will take the corpus and divide it among the most probably topics. Finally, you could use the script in the experiment folder to run the model continously on different parameters and calculate the significance of each model.
