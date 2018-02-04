from pathlib import Path

from tornado import web


PKG_ROOT = Path(__file__).parent.resolve()


class MainHandler(web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def handlers(*,static_path):
    return [
        (r"/", MainHandler),
        (r"/static", web.StaticFileHandler,
         dict(path=static_path)),
        ]


def make_app(settings):
    static_path = settings.pop('static_path', PKG_ROOT / 'static')
    app = web.Application(handlers(static_path=static_path),
                          **settings)
    return app
