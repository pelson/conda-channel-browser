import argparse
import logging

from tornado.ioloop import IOLoop

from .webapp import make_app


_LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("channel_root", help="The URL to the channel root.",
                        default="https://anaconda.org")
    parser.add_argument("--port", help="The port to listen on",
                        default=8080)
    parser.add_argument("--devel", '--debug', help="Development mode",
                        action='store_true')
    args = parser.parse_args()

    logging.basicConfig()

    if args.devel:
        _LOGGER.setLevel(logging.DEBUG)
    else:
        _LOGGER.setLevel(logging.INFO)

    _LOGGER.debug(f'Arguments passed {args!r}')

    app = make_app(settings=dict(channel_root=args.channel_root, debug=args.devel))
    app.listen(args.port)
    _LOGGER.info(f'Listening on {args.port}')

    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        _LOGGER.info('Terminating web application.')
        return
