from lib.preprocessing import preprocess_line_en
import xml.etree.ElementTree as ET
import sys

from shared.constants import DATASET_PATH

class Index(dict):
    def __init__(self,iterable):
        super().__init__(iterable)
        self.docCount = 0

class IndexTerm(dict):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.docFreq = 0

class TermPositions():
    def __init__(self, positions):
        self.positions = positions
        self.freq = len(positions)

def build_index():
    index = Index({})

    with open(DATASET_PATH) as f:
       for _, elem in ET.iterparse(f):
           if elem.tag == "row":
               index.docCount += 1
               text = elem.attrib["Body"]
               doc_id = elem.attrib["Id"]


               terms = preprocess_line_en(text)

               term_idx = 0
               for term in terms:
                    term_idx += 1
                    if term in index:
                        if doc_id in index[term]:
                            index[term][doc_id].positions.append(term_idx)
                        else:
                            index[term][doc_id] = TermPositions([term_idx])
                    else:
                        # Haven't seen this word before
                        index[term] = IndexTerm({doc_id: TermPositions([term_idx])})

    # Calculate and store the document frequencies
    for term in index:
        index[term].docFreq = len(index[term])

    return index

index = []
if 'runserver' in sys.argv:
    index = build_index()
    # # Print the contents of the index
    # for term in sorted(index):
    #     print(f"{term}:{index[term].docFreq}")
    #     for doc in index[term]:
    #         print(f"\t{doc}: {','.join([str(x) for x in sorted(index[term][doc].positions)])}")





if __name__ == "__main__":
    build_index()
