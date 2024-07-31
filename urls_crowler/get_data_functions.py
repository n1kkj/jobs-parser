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


def get_html_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.headers['Content-Type'] in ('text/html; charset=utf-8', 'text/html', 'text/html; charset=UTF-8'):
            return response.text
        else:
            print(f"Ответ не является HTML: {response.headers['Content-Type']}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None
