import requests


def get_json_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.headers['Content-Type'] in ('application/json; charset=utf-8', 'application/json'):
            return response.json()
        else:
            print(f"Ответ не является JSON: {response.headers['Content-Type']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None
