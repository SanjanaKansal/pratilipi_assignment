import requests
import os

content_service_host = os.getenv("CONTENT_SERVICE_HOST", "http://router:80")
CONTENT_SERVICE_BASE_URL = "{}/api/v1/content/".format(content_service_host)


def get_series_from_content_service(title):
    headers = {'Content-Type': 'application/json'}
    params = {'title': title}
    response = requests.get(CONTENT_SERVICE_BASE_URL + "series/", headers=headers, params=params)
    return response.json()


def get_chapter_details_from_content_service(title):
    headers = {'Content-Type': 'application/json'}
    params = {'title': title}
    response = requests.get(CONTENT_SERVICE_BASE_URL + "chapters/", headers=headers, params=params)
    return response.json()
