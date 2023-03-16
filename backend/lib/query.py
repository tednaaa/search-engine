from lib.build_index import index
from lib.preprocessing import preprocess_line_en
from search_engine.models import Document
import math


def run_ranked_search(query):
    words = preprocess_line_en(query)
    scores = {}

    for word in words:
        docs = index.get(word, [" No results"])

        for doc_id in docs:
            score = (1 + math.log10(docs[doc_id].freq)) * \
                math.log10(index.docCount / docs.docFreq)

            if (doc_id in scores):
                scores[doc_id] += score
            else:
                scores[doc_id] = score

    sorted_scores_ids = sorted(scores, key=scores.get, reverse=True)
    sorted_scores = {doc_id: scores[doc_id] for doc_id in sorted_scores_ids}

    return sorted_scores


def run_query(query):
    words = preprocess_line_en(query)

    if not words:
        return []

    nums = []

    if ' and not ' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        all_doc_ids = set([str(doc.doc_id) for doc in Document.objects.all()])
        not_res2 = all_doc_ids.difference(res2)

        nums = res1.intersection(not_res2)
        nums = [int(i) for i in nums]

    elif ' and ' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        nums = res1.intersection(res2)

    elif ' or not ' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        all_doc_ids = set([str(doc.doc_id) for doc in Document.objects.all()])

        not_res2 = all_doc_ids.difference(res2)

        nums = res1.union(not_res2)
        nums = [int(i) for i in nums]

    elif ' or ' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        nums = res1.union(res2)

    else:
        nums = run_ranked_search(query)

    return nums
