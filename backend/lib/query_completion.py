# Copyright Tom Auger 2023

from string import punctuation
import math
import re
from collections import defaultdict
import heapq
import os
import xml.etree.ElementTree as ET

# Update this with your dataset
dataset_file = 'bitcoin.xml'

# Don't change anything below this line
# ------------------------------------

def get_titles(dataset_path):
    titles = []
    with open(dataset_path) as f:
        for _, elem in ET.iterparse(f):
            if elem.tag == "row":
                title = elem.attrib["Title"].strip()
                titles.append(title.translate(str.maketrans('', '', punctuation)).strip().split(' '))
    return titles

def txt_loader(file, listify=True):
    wrapper = open(file,"r",encoding="utf-8-sig")
    data = wrapper.readlines()
    wrapper.close()
    if listify:
        data = [line.translate(str.maketrans('', '', punctuation)).strip().split(' ') for line in data]
    else:
         data = [line.translate(str.maketrans('', '', punctuation)).strip() for line in data]

    return data

# return True if n_gram contains less than n non-stop words, once false, no more items are added
def lenChecker(n_gram,n):
    clean = [tok for tok in n_gram if tok not in stop_words]
    return len(clean)<n
# given an n-gram as a string, returns n
def whatGram(n_gram):
    clean = n_gram.split(' ')
    clean = [tok for tok in clean if tok not in stop_words]
    return len(clean)
def lenChecker2(n_gram,n):
    clean = [tok for tok in n_gram if tok not in stop_words]
    return len(clean)==n
def lenChecker3(n_gram,n):
    clean = [tok for tok in n_gram.split(' ') if tok not in stop_words]
    return len(clean)==n

def build_unigrams(collection):
   # start = time.time()
    unigrams = {}
    for title in collection:
        for word in title:

            if word in stop_words or len(word)==0:
                continue

            if word in unigrams:
                unigrams[word][0]+=1
            else:
                # freq,n
                unigrams[word]=[1,1]
   # end = time.time()
   # print(str(end-start)+': time elapsed(s)')
    return unigrams

def build_bigrams(collection):
    #start=time.time()
    bigrams = {}
    for title in collection:
        # -1 as last token must be in prior bigram only
        for i in range(len(title)-1):
            temp=[]
            if title[i] in stop_words:
                continue
            else:
                temp.append(title[i])
                j=1
            while i+j < len(title) and lenChecker(temp,2):
                succ = title[i+j]
                temp.append(succ)
                j+=1

            if len(temp)>1:
                last = temp[len(temp)-1]
                if last in stop_words:
                    continue
                else:
                    temp = ' '.join(temp)
                    if temp in bigrams:
                        bigrams[temp][0]+=1
                    else:
                        bigrams[temp]=[1,2]
   # end = time.time()
   # print(str(end-start)+': time elapsed(s)')
    return bigrams

def build_trigrams(collection):
   # start=time.time()
    trigrams = {}
    for title in collection:
        # -2 as last 2 tokens must be in prior trigram only
        for i in range(len(title)-2):
            temp=[]
            if title[i] in stop_words:
                continue
            else:
                temp.append(title[i])
                j=1
            while i+j < len(title) and lenChecker(temp,3):
                succ = title[i+j]
                temp.append(succ)
                j+=1

            if len(temp)>1:
                last = temp[len(temp)-1]
                if last in stop_words:
                    continue
                elif not lenChecker2(temp,3):
                    continue;
                else:
                    temp = ' '.join(temp)
                    if temp in trigrams:
                        trigrams[temp][0]+=1
                    else:
                        trigrams[temp]=[1,3]
  #  end = time.time()
  #  print(str(end-start)+': time elapsed(s)')
    return trigrams

# removes stop-words from complete part of query, investigate differences further
def query_splitter(query):
    query = [a for a in query.split(' ') if a]
    # lower tokens
    # query = [a.lower() if a not in lc_blacklist else a for a in query]
    completed = [a for a in query[:-1] if a not in stop_words]
    partial = query[-1:][0]
    return [completed, partial]


def complete(part):
    #start=time.time()
    completions=[]
    for c in list(unigrams.keys()):
        if c.startswith(part):
            completions.append(c)
    #end = time.time()
    # print(str(end-start)+': time elapsed(s)')
    return completions

# returns the total number of documents containing the term
def df(term):
    # only check unigrams
    if phrases[term][1]==1:
        return phrases[term][0]
    else:
        return 0
# returns the inverse domain frequency of a term
# TODO: change small=>titles

# experiment with omitting +1, assuming df>0
def idf(term):
    return math.log(1+k/1+df(term))
# needs to be changed not to use small

def term_completion_prob(term,denom):
    return (df(term)*idf(term))/denom

# n-gram as string
def freq_norm(n_gram):
    return phrases[n_gram][0] / (math.log(averageFreqs[phrases[n_gram][1]]))

# n-gram as string
def term2phrase(n_gram, term):
    #start=time.time()
    if term in n_gram:
        #out = freq_norm(n_gram) / sum([freq_norm(a) for a in t2p[term][0]])
        out = freq_norm(n_gram) / t2p[term][1]
    else:
        out = 0
    #end=time.time()
   # print(end-start)
    return out

## Build Inverted Index for finding the phrases containing a searched term
# {term:[phrase]} containing term

def t2p_build():
    P = {}
    #start = time.time()
    for p in list(phrases.keys()):
        for word in p.split(' '):
            if word in P:
                # p.split(' ')
                P[word].append(p)
            else:
                # p.split(' ')
                P[word] = [p]

    # store sum of freq norm for all phrases relating to a term
    # so this may be accessed by term2phrase and not calculated at runtime
    for k in P:
        P[k] = (P[k],sum([freq_norm(a) for a in P[k]]))
    #end = time.time()
   # print(str(end-start)+': time elapsed(s)')
    return P

# maps terms to docIDs
def t2ID_build():
   # start=time.time()
    idx = {}
    for c1, d in enumerate(titles):
        #tokens = preprocessor(d[0])
        for tok in d:
            if tok in stop_words:
                continue
            if tok in idx:
                # inverted index is dict mapping term to list of docIDs
                idx[tok].add(c1)
            else:
                idx[tok] = {c1}
   # end = time.time()
   # print(str(end-start)+': time elapsed(s)')
    return idx

# returns the docIDs of any documents containing all terms present in an input sequence
# unions the set of docIDs for each term to produce a set containing each term in the phrase
def getIDs(seq):
    phrase = [tok for tok in seq if tok not in stop_words]
    if phrase:
        try:
            out = t2ID[phrase[0]]
        except KeyError:
            return set()
        phrase=phrase[1:]
        if phrase:
            for i in phrase:
                 out = out.intersection(t2ID[i])
    else:
        return set()
    return out

# n-gram as str
def query_correlation(n_gram, full):
    if not any(t in n_gram for t in full):
        return 0

    #start=time.time()
    n_gram_terms = n_gram.split(' ')

    phrase_IDs = getIDs(n_gram_terms)
    full_IDs = getIDs(full)
    if full_IDs:
        check = all([True if word in n_gram else False for word in full])
    else:
        check=False
    if phrase_IDs and check:
        #print(len(phrase_IDs.intersection(full_IDs)))
        #print(len(phrase_IDs))
        out = len(phrase_IDs.intersection(full_IDs))/len(phrase_IDs)
    else:
        out = 0
    #end=time.time()
    #print(str(end-start)+': time elapsed(s)')
    return out

term_regex = re.compile(r'[^\s]+')
def format_completion(completion, term_list):
    html_completion = completion
    html_completion = re.sub(fr"(\s|^)({term_list})*(\w*)", r"\1\2<b>\3</b>", html_completion, flags=re.IGNORECASE)
    return {'text': completion, 'html': html_completion}

def complete_query(query):
    num_results = 8
    if not query:
        return []

    query = query.lower()
    full, partial = query_splitter(query)
    completions = complete(partial)
    # calc ahead of time as denom is constant given query
    denom = sum([df(c)*idf(c) for c in completions])
    # C will hold candidate phrases and their scores
    C=defaultdict(int)
    top_scores = []

    probs = [(c,term_completion_prob(c,denom)) for c in completions]
    comps = sorted(probs, key=lambda x: x[1])[-40:]
    for c, tc_prob in comps:
        # iterate over possible word completions

        for p in t2p[c][0]:
            if len(p) < len(query):
                continue

            if full and not any(t in p for t in full):
                continue

            # for each completion, iterate over all phrases containing the completion
            t2p_prob = term2phrase(p,c)
            if full:
                # If the partial score is already smaller than the top 5 scores then
                # no need to evaluate it
                partial_score = tc_prob * t2p_prob
                if len(top_scores) == num_results and partial_score < top_scores[0]:
                    continue

                qp_corr = query_correlation(p,full)

                score = partial_score * qp_corr
            else:
                 score = tc_prob * t2p_prob

            # Bump up completions that start with the query
            if p.startswith(query):
                score += 1

            # If there is an exact match then push it to the top
            if p == query.strip():
                score += 1

            # add phrase and its score to output
            if score>0 and C[p] < score:
                C[p] = score

                # Keep track of the top 5 scores to avoid processing terms which
                # won't make it into the top 5
                if score >= 1:
                    score -= 1
                if len(top_scores) < num_results:
                    heapq.heappush(top_scores, score)
                else:
                    heapq.heappushpop(top_scores, score)

    query_completions = [c for c in sorted(C, key=C.get, reverse=True)][:num_results]

    return query_completions

def get_path(filename):
    return os.path.join(os.path.dirname(__file__), filename)

stop_words = set(txt_loader(get_path("../lib/datasets/stopwords_en.txt"),False))

titles = get_titles(get_path(f'../lib/datasets/{dataset_file}'))
titles = list(map(lambda x: [y.lower() for y in x if y], titles))
k = len(titles)
averageFreqs = {}

# build unigrams
unigrams = build_unigrams(titles)
averageFreqs[1] = sum([a[0] for a in list(unigrams.values())])/(len(list(unigrams.keys())))

# build bigrams
bigrams = build_bigrams(titles)
averageFreqs[2] = sum([a[0] for a in list(bigrams.values())])/(len(list(bigrams.keys())))

# build trigrams
trigrams=build_trigrams(titles)
averageFreqs[3] = sum([a[0] for a in list(trigrams.values())])/(len(list(trigrams.keys())))

# phrases maps {n-gram:[freq,n]}
phrases = {}
phrases.update(unigrams)
phrases.update(bigrams)
phrases.update(trigrams)

# bigrams and trigrams no longer needed, can be freed from memory, retain unigrams to serve as vocab
del bigrams, trigrams

# build term to [phrase] index
t2p = t2p_build()

# build term to [docID] index
t2ID = t2ID_build()
