from dis import dis
from math import dist
import os
import random
import re
import sys
from pomegranate import *
from numpy.random import choice

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = list(corpus[page])
    if len(links) < 1:
        p = 1 / len(corpus)
        dis = dict()
        for key in corpus:
            dis[key] = p
        return dis
    p = damping_factor / len(links)
    pp = (1-damping_factor)/ len(corpus)
    dist = dict()

    for key in corpus:
        if key in links:
            dist[key] = p + pp
        else:
            dist[key] = pp
    return dist





def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    prob = 1 / len(corpus)
    st = dict()
    for key in corpus:
        st[key] = prob
    dist = []
    for key in corpus:
        t = transition_model(corpus, key, damping_factor)
        for keyy, value in t.items():
            l = []
            l.append(key)
            l.append(keyy)
            l.append(value)
            dist.append(l)

        

    d1 = DiscreteDistribution(st)
    d2 = ConditionalProbabilityTable(dist,[d1])

    model = MarkovChain([d1,d2])
    
    final = model.sample(n)
    f = len(final)
    r = dict()
    for key in corpus:
        r[key] = final.count(key) / f
    return r
    


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    dist = dict()
    control = dict()
    cc = dict()
    le = len(corpus)
    for key in corpus:
        dist[key] = 1/le
        control[key] = dist[key]
        cc[key] = 1
    
    f = 0
    sm = 0.001 * len(control)
    while sum(cc.values()) > sm :
        i = list()
        c = random.choice(list(dist.keys()))
        for key in corpus:
            if c in corpus[key]:
                i.append(key)
        s= 0
        for key in i:
            s += (dist[key] /len(corpus[key]))

        dist[c] = ((1-damping_factor)/ le) + damping_factor * s
        cc[c] = abs(control[c] - dist[c])
        control[c] = dist[c]
    return dist

        



if __name__ == "__main__":
    main()
