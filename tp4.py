import os
import math
from preprocces import preprocess
from load_index import load_index

# Read the ranked results from the file
def read_ranked_results(file_path):
    ranked_results = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            query_id, doc_id, score = map(float, line.strip().split(','))
            if query_id not in ranked_results:
                ranked_results[query_id] = []
            ranked_results[query_id].append((int(doc_id), score))
    return ranked_results

# Read the preprocessed document from the collection
def read_preprocessed_document(doc_id, collection):

    return collection[doc_id]  


# Calculate TF-IDF scores for terms in documents
def calculate_tfidf(doc, collection):
    terms = doc.split()

    tfidf_scores = {}
    N = len(collection)
    # Calculate TF-IDF for each term in the document
    for term in terms:
        tf = terms.count(term)
        if term not in tfidf_scores:
            # Calculate document frequency of the term from the index
            df=1
            # df=index[term]['doc_freq']
            idf = math.log10(N / df) if df != 0 else 0
            tfidf_score = (1 + math.log10(tf)) * idf
            tfidf_scores[term] = tfidf_score

    return tfidf_scores


# Retrieve top n_t terms based on TF-IDF scores
def retrieve_top_terms(tfidf_scores, n_t):
    sorted_terms = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
    top_terms = [term for term, _ in sorted_terms[:n_t]]
    return top_terms

# Write the expanded query to a file
def write_expanded_query(query_id, query_terms,expanded_terms, output_file):
    base_path = ""
    new_path = os.path.join(base_path, output_file)
    with open(new_path, 'a') as file:
        file.write(f"{query_id} {query_terms} {'+'} {' '.join(expanded_terms)}\n")

# Main function to perform query expansion for each query
def perform_query_expansion(rank_file, collection, queries, n_d, n_t):
    ranked_results = read_ranked_results(rank_file)
    for query in queries:
        query_id, query_text = query.split(',', 1)
        top_documents = ranked_results[int(query_id)][:n_d]
        combined_documents = [read_preprocessed_document(doc_id, collection) for  doc_id, _ in top_documents]
        combined_documents = [element for sous_liste in combined_documents for element in sous_liste]
        combined_text = ' '.join(combined_documents)
        tfidf_scores = calculate_tfidf(combined_text,collection)
        top_terms = retrieve_top_terms(tfidf_scores, n_t)
        write_expanded_query(query_id, query_text,top_terms, f"Qm.{n_d}.{n_t}.txt")



# Given inputs
ranked_results_file ="tfidf-chatgpt4.results.txt"

file_path ="Chat-GPT4-ANSWERS/ChatGPT4_answers.txt"
collection_preprocessed={}
with open(file_path, 'r', encoding='utf-8') as file:
    current_document = ""
    lines=file.readlines()
    for line in lines:
        if line.startswith("ID: "):
            id=(int)(line[4:-1])
        if line.startswith("TEXT: "):
            current_document = line.replace("TEXT: ", "").strip()  # Extraction du texte
            preprocessed_doc=preprocess(current_document,True,True)
            collection_preprocessed[id]=preprocessed_doc


queries = [
    "1,Drawing closed polygons from simple lines",
    "2,Using njit with sympy.Piecewise lambdified functions",
    "3,Error while Using WebSecurityConfigurerAdapter class for Spring Boot Security",
    "4,SSL HandShake Exception:No appropriate protocol (protocol is disabled or cipher suites are inappropriate)",
    "5,CXF wsdl2java throws class generation name collision in object factory",
    "6,Trying to compile a code in VSCode using g++ and getting an error",
    "7,Dealing with endianess in Kotlin",
    "8,NextJs app route SSR doesn&#39;t clear the old data on redux",
    "9,React Native - Long press and pan/swipe to select element",
    "10,How can I target an iframe that&#39;s on a seperate HTML file"
]
# ranked_results = read_ranked_results(ranked_results_file)
# combined_documents = [read_preprocessed_document(id, collection_preprocessed) for id in[1,2,3]]
# combined_documents = [element for sous_liste in combined_documents for element in sous_liste]
# combined_text = ' '.join(combined_documents)
# print(combined_text)
# tfidf=calculate_tfidf(combined_text,collection_preprocessed)
# print(retrieve_top_terms(tfidf,5))
# for query in queries:
#     query_id, query_text = query.split(',', 1)
#     top_documents = ranked_results[int(query_id)][:2]
#     print(top_documents)

n_d = 1  # Top n_d documents
n_t = 5  # Top n_t terms

# Perform query expansion and write to files
for n_d in [1,3,5]:
    for n_t in [1,5,10]:
        perform_query_expansion(ranked_results_file, collection_preprocessed, queries, n_d, n_t)
