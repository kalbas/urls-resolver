from http import HTTPStatus
import unittest

from requests.exceptions import ReadTimeout

from const import URL_PATHS_MAP, SERVER_HOST, SERVER_PORT
from resolver import resolve_url, MaxDepthExceeded, CircularDependencyFound


class TestUrlResolving(unittest.TestCase):
    HOST = 'http://{}:{}'.format(SERVER_HOST, SERVER_PORT)

    def test_url_found_successful(self):
        source_path = '/forth-transition-url'
        source_url = '{}{}'.format(self.HOST, source_path)

        response = resolve_url(source_url)

        self.assertEqual(response.url, '{}{}'.format(self.HOST, URL_PATHS_MAP[source_path]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_cycle_will_broken(self):
        with self.assertRaises(CircularDependencyFound):
            resolve_url('{}/first-cycled-transition-url'.format(self.HOST))

    def test_max_depth_exceeded(self):
        with self.assertRaises(MaxDepthExceeded):
            resolve_url('{}/first-transition-url'.format(self.HOST))

    def test_url_not_found(self):
        source_url = '{}/nonexistent-url'.format(self.HOST)
        response = resolve_url(source_url)
        self.assertEqual(response.url, source_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_url_not_respond(self):
        with self.assertRaises(ReadTimeout):
            resolve_url('{}/timeout-url'.format(self.HOST))

    def test_manage_to_infinite_response_content(self):
        source_url = '{}/first-infinite-content-url'.format(self.HOST)
        response = resolve_url(source_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertFalse(response._content_consumed)
        # Вот так в тестах конечно делать нельзя наверное. У requests content -- это проперти.
        # Так вот мы сначала проверили, что респонс получили с нужным статус кодом,
        # затем проверили, что контент не весь употребили, затем с помощью вызова проперти
        # употребли и догрузили недотающие чанки, затем проверили, что все употребили
        response.content
        self.assertTrue(response._content_consumed)
