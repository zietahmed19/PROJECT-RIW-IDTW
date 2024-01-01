from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import nltk.downloader

# Create a Downloader object
downloader = nltk.downloader.Downloader()

# downloader.download('stopwords')




# Load the stopwords list
stopwords = stopwords.words('english')
# print(stopwords)


# Preprocessing function
def preprocess(text, use_stemming=True, use_stopping=True):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove punctuation
    tokens = [token.translate(str.maketrans('', '', string.punctuation)) for token in tokens]

    # Apply stemming if enabled
    if use_stemming:
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]

    # Apply stopping if enabled
    if use_stopping:
        tokens = [token for token in tokens if token not in stopwords]
    
    tokens = [token for token in tokens if token != '']
    return tokens