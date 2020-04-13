from http import HTTPStatus
from http.server import HTTPServer, BaseHTTPRequestHandler
import time

from const import SERVER_HOST, SERVER_PORT, URL_PATHS_MAP, INFINITE_CHUNK, REQUEST_TIMEOUT


class BadlyConfiguredHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        # Да сразу закроем метод HEAD, чего уж там
        self.send_response(HTTPStatus.METHOD_NOT_ALLOWED, message='You shall not pass')
        self.end_headers()

    def do_GET(self):
        if self.path not in URL_PATHS_MAP.keys():
            self.send_response(HTTPStatus.NOT_FOUND)
        elif URL_PATHS_MAP[self.path] is not None:
            self._redirect_to_next_url()

        elif self.path == '/timeout-url':
            time.sleep(REQUEST_TIMEOUT + 1)
        else:
            self.send_response(HTTPStatus.OK, message='OK')

        self.end_headers()
        if self.path == '/first-infinite-content-url':
            self._send_lots_of_chunks()

    def _redirect_to_next_url(self):
        self.send_response(HTTPStatus.MOVED_PERMANENTLY)
        # В продакшене я бы конечно рассмотрел сбор/разбор урлов с помощью urlsplit
        # и urlunsplit из urllib. Здесь же пример простой, по факту прыгаем
        # с path на path одно и того же хоста
        self.send_header(
            'Location',
            'http://{}:{}{}'.format(SERVER_HOST, SERVER_PORT, URL_PATHS_MAP[self.path])
        )

    def _send_lots_of_chunks(self):
        for i in range(10):
            time.sleep(.5)
            self.wfile.write(INFINITE_CHUNK)


def run(server_class=HTTPServer, handler_class=BadlyConfiguredHTTPRequestHandler):
    # Сервер тоже нужно конфигурировать по людски в продакшене, а не вот так вот константами
    server_address = (SERVER_HOST, SERVER_PORT)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == "__main__":
    run()
