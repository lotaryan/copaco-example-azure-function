import json
import logging
import requests
import azure.functions as func


def get_all_authors_with_les():
    authors = []
    current_page = 1
    total_pages = 1

    def get_one_page():
        nonlocal current_page
        response = requests.get(f'https://api.quotable.io/authors?order=asc&limit=150&page={current_page}')
        if response.status_code == 200:
            nonlocal total_pages
            response_json = response.json()
            total_pages = response_json["totalPages"]
            for author in response_json["results"]:
                if "les" in author["name"]:
                    authors.append(author["slug"])
            current_page += 1
        else:
            raise Exception("Connection error with api")

    while current_page <= total_pages:
        get_one_page()

    return authors


def get_all_quotes_by_authors(authors):
    author_quote = {}
    current_page = 1
    total_pages = 1

    def get_one_page():
        nonlocal current_page

        response = requests.get(
            f'https://api.quotable.io/quotes?author={"|".join(authors)}&page={current_page}&limit=150')
        if response.status_code == 200:
            nonlocal total_pages
            response_json = response.json()
            total_pages = response_json["totalPages"]
            for quote in response_json["results"]:
                if not author_quote.get(quote["author"]):
                    author_quote[quote["author"]] = []
                author_quote[quote["author"]].append(quote["content"])
            current_page += 1
        else:
            raise Exception("Connection error with api")

    while current_page <= total_pages:
        get_one_page()

    return author_quote


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        print(get_all_quotes_by_authors(get_all_authors_with_les()))
        return func.HttpResponse(json.dumps(get_all_quotes_by_authors(get_all_authors_with_les())),
                                 mimetype="application/json")
    except Exception as e:
        logging.error(f'failed with error {e}.')
        return func.HttpResponse(
            "Unexpected issues",
            status_code=500
        )
