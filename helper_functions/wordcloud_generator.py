import matplotlib.pyplot as plt
from wordcloud import *
"""
Minimal Example
===============
Generating a square wordcloud from the US constitution using default arguments.
"""

import random
# def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
#     return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    print "hsl(0, 0%%, %d%%)" % random.randint(60, 100)
    return "hsl(1, 0%%, %d%%)" % random.randint(60, 100)

def cloud_with_frequency(text, filename, show):
    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(max_font_size=250, relative_scaling=.5, width=1024, height=768, color_func=random_color_func, background_color="black").generate(text)
    plt.figure()
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(filename + 'v2')
    if show:
        plt.show()

import os
d = "C:/Users/Qingkai.Li/PycharmProjects/LDA_EXPERIMENT/wordcloud/"
if not os.path.exists(d):
    os.makedirs(d)

def wordcloud(text, filename, show = False):
    # Generate a word cloud image
    wordcloud = WordCloud(width=1680, height=1050, color_func=random_color_func, background_color="white").generate(text)
    # Display the generated image
    plt.imshow(wordcloud)
    plt.axis("off")

    print "Wordcloud created: ", filename
    plt.savefig(d + filename + " v1")

    if show:
        plt.show()
    else:
        plt.close()

    cloud_with_frequency(text, d + filename, show)

# test_string = "To assess the effects of ischemic preconditioning (IPC, 10-min ischemia/10-min reperfusion) on steatotic liver mitochondrial function after normothermic ischemia-reperfusion injury (IRI). METHODS: Sixty male Sprague-Dawley rats were fed 8-wk with either control chow or high-fat/high-sucrose diet inducing > 60% mixed steatosis. Three groups (n = 10/group) for each dietary state were tested: (1) the IRI group underwent 60 min partial hepatic ischemia and 4 h reperfusion; (2) the IPC group underwent IPC prior to same standard IRI; and (3) sham underwent the same surgery without IRI or IPC. Hepatic mitochondrial function was analyzed by oxygraphs. Mitochondrial Complex-I, Complex-II enzyme activity, serum alanine aminotransferase (ALT), and histological injury were measured. RESULTS: Steatotic-IRI livers had a greater increase in ALT (2476 +/- 166 vs 1457 +/- 103 IU/L, P < 0.01) and histological injury following IRI compared to the lean liver group. Steatotic-IRI demonstrated lower Complex-I activity at baseline [78.4 +/- 2.5 vs 116.4 +/- 6.0 nmol/(min.mg protein), P < 0.001] and following IRI [28.0 +/- 6.2 vs 104.3 +/- 12.6 nmol/(min.mg protein), P < 0.001]. Steatotic-IRI also demonstrated impaired Complex-I function post-IRI compared to the lean liver IRI group. Complex-II activity was unaffected by hepatic steatosis or IRI. Lean liver mitochondrial function was unchanged following IRI. IPC normalized ALT and histological injury in steatotic livers but had no effect on overall steatotic liver mitochondrial function or individual mitochondrial complex enzyme activities. CONCLUSION: Warm IRI impairs steatotic liver Complex-I activity and function. The protective effects of IPC in steatotic livers may not be mediated through mitochondria."
# wordcloud(test_string, "test")