SERVER_HOST = 'localhost'
SERVER_PORT = 8000

URL_PATHS_MAP = {
    '/first-transition-url': '/second-transition-url',
    '/second-transition-url': '/third-transition-url',
    '/third-transition-url': '/forth-transition-url',
    '/forth-transition-url': '/fifth-transition-url',
    '/fifth-transition-url': None,

    '/first-cycled-transition-url': '/second-cycled-transition-url',
    '/second-cycled-transition-url': '/third-cycled-transition-url',
    '/third-cycled-transition-url': '/first-cycled-transition-url',

    '/first-infinite-content-url': None,

    '/timeout-url': None,
}
INFINITE_CHUNK = b'This is a big chunk'

MAX_DEPTH = 5
MAX_RESPONSE_CONTENT_LENGTH = 16
REQUEST_TIMEOUT = 5
