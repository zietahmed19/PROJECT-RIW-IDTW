import math
from pprint import pprint
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from collections import defaultdict
import xml.etree.ElementTree as ET


def preprocess(documents):
    ps = PorterStemmer()

    def stem_tokens(document):
        tokens = word_tokenize(document.lower())
        return [ps.stem(token) for token in tokens]

    return list(map(stem_tokens, documents))


def generate_index(preprocessed_documents):
    index = defaultdict(dict)
    for doc_id, document in enumerate(preprocessed_documents):
        for term in document:
            if term not in index:
                index[term] = {"df": 0, "posting_list": {}}
            if doc_id not in index[term]["posting_list"]:
                index[term]["posting_list"][doc_id] = 0
                index[term]["df"] += 1
            index[term]["posting_list"][doc_id] += 1
    return index


class Document:
    def __init__(self, id, terms):
        self.id = id
        self.terms = terms
        self.length = self.calculate_length()

    def calculate_length(self):
        return math.sqrt(sum(tf**2 for tf in self.terms.values()))


def parse_txt(txt_file_path):
    tree = ET.parse(txt_file_path)
    root = tree.getroot()
    documents = [doc.find("TEXT").text for doc in root.findall("DOC")]
    return documents


class Query(Document):
    def __init__(self, terms):
        super().__init__(-1, terms)


class SearchEngine:
    def __init__(self, documents):
        self.documents = documents

    def tf_idf(self, term, document):
        tf = document.terms.get(term, 0)
        df = sum(term in doc.terms for doc in self.documents)
        idf = math.log10(len(self.documents) / df) if df else 0
        return tf * idf

    def cosine_score(self, query):
        scores = []
        for doc in self.documents:
            numerator = sum(
                self.tf_idf(term, doc) * self.tf_idf(term, query)
                for term in query.terms
            )
            denominator = doc.length * query.length
            score = numerator / denominator if denominator else 0
            scores.append((doc.id, score))
        return sorted(scores, key=lambda x: x[1], reverse=True)[:10]


def parse_txt(txt_file_path):
    print(txt_file_path)
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        documents = file.read().split('\n')  # Split documents by newline
    return documents

txt_file_path ="Chat-GPT4-ANSWERS/ChatGPT4_answers.txt"
print(f"hello============================================== {txt_file_path}")

# Define your documents and query here
documents = parse_txt(txt_file_path)
query = "What does the &quot;yield&quot; keyword do in Python?"

# Preprocess the documents
preprocessed_documents = preprocess(documents)

# Generate the index
index = generate_index(preprocessed_documents)
pprint(index)

# Create Document objects
documents = [
    Document(
        id,
        {
            term: index[term]["posting_list"][id]
            for term in index
            if id in index[term]["posting_list"]
        },
    )
    for id in range(len(preprocessed_documents))
]


# Create the search engine
search_engine = SearchEngine(documents)

# Preprocess the query
query_terms = preprocess([query])[0]

# Create a dictionary of term frequencies
query_tf = {term: query_terms.count(term) for term in query_terms}

# Create the Query object
query = Query(query_tf)


# Get the cosine scores
scores = search_engine.cosine_score(query)

# Print the query
print('Query: "{}"'.format(" ".join(query.terms)))

# Print the results
print("Top 10 documents for the query:")
for doc_id, score in scores:
    print("Document ID: {}, Score: {}".format(doc_id, score))
    scores = search_engine.cosine_score(query)

# Print and save the results
results_file_path = 'tfidf-chatgpt4.txt'
with open(results_file_path, 'w') as file:
    print('Query: "{}"'.format(" ".join(query.terms)))
    file.write('Query: "{}"\n'.format(" ".join(query.terms)))

    print("Top 10 documents for the query:")
    file.write("Top 10 documents for the query:\n")
    
    for doc_id, score in scores:
        print("Document ID: {}, Score: {}".format(doc_id, score))
        file.write("Document ID: {}, Score: {}\n".format(doc_id, score))
