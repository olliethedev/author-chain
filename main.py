import os
import requests
import time
from pathlib import Path
from langchain.chains import SequentialChain
from chains import get_author_chain, get_editor_chain, get_question_chain, get_writer_chain, get_title_chain, get_description_chain, get_title_chain, get_description_chain
from data_loaders import get_input_articles, get_questions_answers

root_folder = "output"

def create_article(topic):
    articles = get_input_articles(topic)
    print(articles)

    output_root = create_output_folder()
    save_to_file(output_root, 'sources.json', str(articles))

    summaries = get_summaries(articles)

    author_chain = get_author_chain()
    question_chain = get_question_chain()

    first_chain = SequentialChain(chains=[author_chain, question_chain],
                                  input_variables=["summaries"],
                                  output_variables=["article", "questions"],
                                  verbose=True)

    first_draft = first_chain({"summaries": summaries})
    save_to_file(output_root, 'first_draft.md', first_draft['article'])

    article = first_draft['article']
    questions = first_draft['questions']
    print(questions)

    extra_data = get_questions_answers(questions)
    save_to_file(output_root, 'extra_data.md', extra_data)

    writer_chain = get_writer_chain()
    editor_chain = get_editor_chain()

    second_chain = SequentialChain(chains=[writer_chain, editor_chain],
                                  input_variables=["article", "extra_information"],
                                  output_variables=["final_draft", "tldr"],
                                  verbose=True)

    final_draft = second_chain({
        "article": article,
        "extra_information": extra_data
    })

    print(final_draft)

    save_to_file(output_root, 'final_article.md', final_draft["final_draft"])
    save_to_file(output_root, 'tldr.md', final_draft["tldr"])

def process_folder(folder):
    if Path.joinpath(Path(root_folder), folder, 'summary.json').exists():
        print("skipping")
        return

    tldr = read_file(Path.joinpath(Path(root_folder), folder, 'tldr.md'))
    article = read_file(Path.joinpath(Path(root_folder), folder, 'final_article.md'))

    seo_data = get_seo_data(article)
    print(seo_data)

    #Replace with your API

    # create_article_request = create_article_post_request(seo_data, tldr, article)
    # y = requests.post('http://localhost:5000/api/v1/articles', json=create_article_request)
    # save_to_file(Path.joinpath(Path(root_folder), folder), 'summary.json', y.text)
    save_to_file(Path.joinpath(Path(root_folder), folder), 'summary.json', str({"seo":seo_data, "tldr":tldr, "article":article}))


def create_output_folder():
    if not os.path.exists(root_folder):
        os.mkdir(root_folder)

    work_folder = str(int(time.time()))
    output_root = Path.joinpath(Path(root_folder), work_folder)
    os.mkdir(output_root)
    return output_root

def save_to_file(output_root, file_name, content):
    with open(Path.joinpath(output_root, file_name), 'w') as f:
        f.write(content)

def get_summaries(articles):
    return '\n'.join([article['summary'] for article in articles])

def get_folders():
    folders = [f for f in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, f))]
    folders.sort()
    return folders

def read_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def get_seo_data(article):
    title_chain = get_title_chain(article)
    description_chain = get_description_chain(article)

    seo_chain = SequentialChain(chains=[title_chain, description_chain],
                                input_variables=[],
                                output_variables=["title", "description"],
                                verbose=True)
    return seo_chain({"inputs":[]})
