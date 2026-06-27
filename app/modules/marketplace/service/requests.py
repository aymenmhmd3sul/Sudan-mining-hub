from app.modules.marketplace.repository.requests_repo import insert_request, fetch_requests


def create_request(user_id: str, title: str, category: str):
    return insert_request(user_id, title, category)


def get_requests():
    return fetch_requests()
