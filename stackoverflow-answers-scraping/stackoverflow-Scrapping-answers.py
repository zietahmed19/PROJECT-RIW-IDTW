import requests
import csv
from bs4 import BeautifulSoup

def fetch_questions(tag, pagesize=5, page=1):
    api_url = f"https://api.stackexchange.com/2.2/questions"
    params = {
        'order': 'desc',
        'sort': 'votes',
        'tagged': tag,
        'site': 'stackoverflow',
        'pagesize': pagesize,
        'page': page,
        'filter': 'withbody'
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching questions for tag '{tag}': {response.status_code}")
        return None

def fetch_answers(question_id):
    api_url = f"https://api.stackexchange.com/2.2/questions/{question_id}/answers"
    params = {
        'order': 'desc',
        'sort': 'votes',
        'site': 'stackoverflow',
        'filter': 'withbody',
        'pagesize': 5
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching answers for question {question_id}: {response.status_code}")
        return None

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def save_questions_to_csv(data, filename, tag, mode='a'):
    with open(filename, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode == 'w':  # Write header only if it's a new file
            writer.writerow(['Tag', 'Question ID', 'Question Title', 'Question Link', 'Question Votes'])

        for question in data['items']:
            writer.writerow([tag, question['question_id'], question['title'], question['link'], question['score']])

def save_answers_to_csv(data, filename, mode='a'):
    with open(filename, mode, newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if mode == 'w':  # Write header only if it's a new file
            writer.writerow(['Question ID', 'Answer ID', 'Answer Score', 'Answer Text'])

        for question in data['items']:
            question_id = question['question_id']
            answers_data = fetch_answers(question_id)
            if answers_data:
                for answer in answers_data['items']:
                    answer_text = html_to_text(answer['body'])
                    writer.writerow([question_id, answer['answer_id'], answer['score'], answer_text])

def process_tags(tags):
    questions_filename = "stackoverflow-answers-scraping/stackoverflow_questions.csv"
    answers_filename = "stackoverflow-answers-scraping/stackoverflow_answers.csv"

    first_tag = True  # Flag to check if it's the first tag

    for tag in tags:
        print(f"Processing tag: {tag}")
        questions_data = fetch_questions(tag)
        if questions_data:
            if first_tag:
                save_questions_to_csv(questions_data, questions_filename, tag, 'w')  # Write mode for the first tag
                save_answers_to_csv(questions_data, answers_filename, 'w')  # Write mode for the first tag
                first_tag = False
            else:
                save_questions_to_csv(questions_data, questions_filename, tag, 'a')  # Append mode for subsequent tags
                save_answers_to_csv(questions_data, answers_filename, 'a')  # Append mode for subsequent tags
        else:
            print(f"No data to save for tag: {tag}")

# Example usage
tags = ['python', 'javascript', 'java', 'c#', 'php']  # Add more tags as needed
process_tags(tags)
