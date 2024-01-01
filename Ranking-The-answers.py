import openai
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set your OpenAI API key
openai.api_key = "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"

# Function to read answers from a text file
def read_answers_from_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.readlines()

# Path to the text file containing answers
answers_file_path = "ChatGPT4_answers.txt"

# Read answers from the text file
answers = read_answers_from_file(answers_file_path)

nltk.download('stopwords')

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

# Function to retrieve the best answer based on a user query
def get_best_answer(user_query):
    user_query = preprocess_text(user_query)
    query_vector = vectorizer.transform([user_query])
    
    # Calculate cosine similarity between the query and answers
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    
    # Get the index of the most similar answer
    best_answer_index = similarities.argmax()
    
    return answers[best_answer_index]

if __name__ == "__main__":
    while True:
        user_query = input("Ask a question (or 'exit' to quit): ")
        if user_query.lower() == "exit":
            break

        # Get the best answer using information retrieval
        best_answer = get_best_answer(user_query)

        # Ask ChatGPT-4 for additional details
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Can you provide more details about this?\n{best_answer}\n\nAnswer:",
            max_tokens=100,  # Adjust as needed
        )

        chatgpt_answer = response.choices[0].text.strip()

        print(f"Best Answer (IR): {best_answer}")
        print(f"ChatGPT-4 Answer: {chatgpt_answer}\n")
