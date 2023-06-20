import logging
import requests
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    response = requests.get('https://api.quotable.io/random')
    if response.status_code == 200:
        print(response.json())
        quote = response.json().get("content", "")
        return func.HttpResponse(quote)
    else:
        return func.HttpResponse(
            "Unexpected issues with random quotes",
            status_code=500
        )
