import requests
import csv

# List of programming languages/tags to search for
tags = ["python", "java", "c++", "javascript", "c#", "php", "android", "jquery", "html", "css"]

# Number of questions to retrieve for each tag (adjust as needed)
num_questions_to_retrieve = 100

# Initialize a CSV file to store the data
csv_file = "stackoverflow_errors.csv"

# Create a CSV file and write the header
with open(csv_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Tag", "Question"])

# Function to retrieve questions for a specific tag
def retrieve_questions(tag):
    base_url = f"https://api.stackexchange.com/2.2/questions"
    params = {
        "tagged": tag,
        "site": "stackoverflow",
        "pagesize": num_questions_to_retrieve,
        "order": "desc",
        "sort": "activity",
        "filter": "withbody"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        for item in data["items"]:
            question_text = item["title"]
            with open(csv_file, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([tag, question_text])

        print(f"Retrieved questions for tag: {tag}")

    except Exception as e:
        print(f"Error retrieving questions for tag {tag}: {str(e)}")

# Retrieve questions for each tag
for tag in tags:
    print(f"Retrieving questions for tag: {tag}")
    retrieve_questions(tag)

print("Data retrieval completed. Data saved to", csv_file)
