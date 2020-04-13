import argparse
from http import HTTPStatus

import requests

from const import MAX_DEPTH, MAX_RESPONSE_CONTENT_LENGTH, REQUEST_TIMEOUT


class MaxDepthExceeded(Exception):
    pass


class CircularDependencyFound(Exception):
    pass


def resolve_url(url):
    # Строго говоря, requests сам умеет обрабатывать множественные редиректы,
    # но в этот раз мы ему запретим, иначе в тестовом задании можно ничего не делать :)
    # (requests может обработать и циклические, потому что при обходе хостов в случае наличия цикла
    # будет наращиваться history список, в котором элементы не проверяются на уникальность
    # и рано или поздно максимально допустимое количество редиректов будет накоплено)
    next_location = url
    urls_history = {next_location}
    while len(urls_history) < MAX_DEPTH:
        response = get_response(next_location)
        next_location = response.headers.get('Location')
        if next_location is None:
            return response
        elif next_location not in urls_history:
            urls_history.add(next_location)
        else:
            raise CircularDependencyFound
    raise MaxDepthExceeded


def get_response(url):
    response = requests.head(url, allow_redirects=False, stream=True, timeout=REQUEST_TIMEOUT)
    if response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
        response = requests.get(url, allow_redirects=False, stream=True, timeout=REQUEST_TIMEOUT)
        # Читаем чанк и уходим отсюда сразу, весь контент не читаем
        response.raw.read(MAX_RESPONSE_CONTENT_LENGTH)
    return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url which will resolved')
    args = parser.parse_args()
    response = resolve_url(args.url)
    print('Request on url: {} returned status code: {}'.format(response.url, response.status_code))
