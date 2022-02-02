import math
import nltk
import sys
import os
import string

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}
    for filename in os.listdir(directory):
        with open(os.path.join(directory,filename)) as f:
            files[filename] = f.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    L = []
    for word in nltk.tokenize.word_tokenize(document):
        if word in nltk.corpus.stopwords.words("english"):
            continue
        p = [e for e in word if e in string.punctuation]
        if len(p) != 0:
            for c in p:
                word.replace("c","")
        L.append(word)
    return L
        


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = {}

    for key,values in documents.items():
        for value in values:
            words[value] = words.get(value,0) + 1
    for word in words:
        words[word] = math.log(len(documents)/ words[word])
    return words
    
            



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    L= {}
    tfidf = {}
    for filename in files:
        freq = {}
        for word in query:
            if word in files[filename]:
                freq[word] = freq.get(word,0) + 1
        tfidf[filename] = freq
    for file in tfidf:
        for word in tfidf[file]:
            if tfidf[file][word] is None:
                continue
            tfidf[file][word] *= idfs[word]

        for word in tfidf[file]:
            L[file] = L.get(file,0) + tfidf[file][word]
     
    final = sorted(L.items(), key = lambda x:x[1], reverse=True)

    LL = []

    for f in final:
        LL.append(f[0])
    
    return LL[:n]

    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentencecsF = {}
    for word in query:
        for sentence in sentences:
            if word in sentence:
                sentencecsF[sentence] = sentencecsF.get(sentence, 0) + idfs.get(word.lower(), 0)
    finalS = sorted(sentencecsF.items(), key = lambda x:x[1], reverse=True)
    L = []
    for s in finalS:
        L.append(s)
    return L[:n]


    


if __name__ == "__main__":
    main()
