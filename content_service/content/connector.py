import os
import requests

user_and_dp_service_host = os.getenv("USER_DP_SERVICE_HOST", "http://router:80")
USER_AND_DP_SERVICE_BASE_URL = "{}/api/v1/".format(user_and_dp_service_host)


def get_user_from_user_service(user_id):
    headers = {'Content-Type': 'application/json'}
    params = {'id': user_id}
    response = requests.get(USER_AND_DP_SERVICE_BASE_URL + "user/", headers=headers, params=params)
    return response.json()


def get_unlocked_chapters_for_user(user_id):
    headers = {'Content-Type': 'application/json'}
    params = {'user_id': user_id}
    response = requests.get(USER_AND_DP_SERVICE_BASE_URL + "daily_pass/", headers=headers, params=params)
    return response.json()
