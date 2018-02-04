from logging import getLogger
from pathlib import Path

from html5print import HTMLBeautifier
from jinja2 import Environment, FileSystemLoader
from tornado import web


_LOGGER = getLogger(__name__)


PKG_ROOT = Path(__file__).parent.resolve()


class BaseHandler(web.RequestHandler):
    def render(self, tmpl_name, **context):
        env = self.settings['template_env']
        template = env.get_template(tmpl_name)
        content_raw = template.render(**context)
        content = HTMLBeautifier.beautify(content_raw, 2)
        return content


class IndexHandler(BaseHandler):
    def get(self):
        self.write(self.render('index.html.tmpl'))


def handlers(*,static_path):
    return [
        (r"/", IndexHandler),
        (r"/static", web.StaticFileHandler,
         dict(path=static_path)),
        ]


def make_app(settings):
    static_path = settings.pop('static_path', PKG_ROOT / 'static')

    template_dir = settings.pop('templates_dir', PKG_ROOT / 'templates')
    env = Environment(loader=FileSystemLoader([template_dir]))
    _LOGGER.debug(f'Template directory {template_dir}')

    settings['template_env'] = env

    app = web.Application(handlers(static_path=static_path),
                          **settings)
    return app
