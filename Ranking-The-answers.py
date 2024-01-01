import openai
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



# Sample user query (you can replace this with a user's query)
user_query = "Drawing closed polygons from simple lines."

# Path to the text file containing answers
answers_file_path = "ChatGPT4_answers.txt"

# Function to read answers from a text file
def read_answers_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()

# Read answers from the text file
answers = read_answers_from_file(answers_file_path)
print(answers)

# Preprocess and tokenize the text
nltk.download("punkt")
stopwords = set(nltk.corpus.stopwords.words("english"))

def preprocess_text(text):
    text = text.lower()
    text = "".join([char for char in text if char not in string.punctuation])
    tokens = nltk.word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords]
    return " ".join(tokens)

preprocessed_answers = [preprocess_text(answer) for answer in answers]

# Calculate TF-IDF vectors for answers
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_answers)

# Calculate cosine similarity between the user query and answers
user_query = preprocess_text(user_query)
query_vector = vectorizer.transform([user_query])
similarities = cosine_similarity(query_vector, tfidf_matrix)

# Find the index of the best-ranked answer
best_answer_index = similarities.argmax()

# Get the best-ranked answer
best_answer = answers[best_answer_index]

# Save the best answer to a text file
best_answer_file_path = "best_answer.txt"
with open(best_answer_file_path, "w", encoding="utf-8") as best_answer_file:
    best_answer_file.write(best_answer)

print("The best answer has been saved to best_answer.txt")
