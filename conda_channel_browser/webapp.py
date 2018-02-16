from logging import getLogger
from pathlib import Path

from html5print import HTMLBeautifier
from jinja2 import Environment, FileSystemLoader
from tornado import web

from .contexts import Channel

_LOGGER = getLogger(__name__)


PKG_ROOT = Path(__file__).parent.resolve()


class BaseHandler(web.RequestHandler):
    def render(self, tmpl_name, **context):
        env = self.settings['template_env']
        template = env.get_template(tmpl_name)
        content_raw = template.render(**context)
#        content = HTMLBeautifier.beautify(content_raw, 2)
        content = content_raw
        return content


class IndexHandler(BaseHandler):
    def get(self):
        self.write(self.render('index.html.tmpl'))


class ChannelHandler(BaseHandler):
    def get(self, channel):
        context_cls = self.settings['contexts']['channel']
        channel = self.settings['channel_root'] + '/' + channel
        _LOGGER.info(f'Creating channel context for {channel}')
        # TODO: cache the channel...
        channel = context_cls.from_channel(channel)
        self.write(self.render('channel.html.tmpl', channel=channel))


def handlers(*,static_path):
    return [
        (r"/", IndexHandler),
        (r"/channel/([a-zA-Z\-]+)", ChannelHandler),
        (r"/static", web.StaticFileHandler,
         dict(path=static_path)),
        ]


def make_app(settings):
    static_path = settings.pop('static_path', PKG_ROOT / 'static')

    template_dir = settings.pop('templates_dir', PKG_ROOT / 'templates')
    env = Environment(loader=FileSystemLoader([template_dir]))
    _LOGGER.debug(f'Template directory {template_dir}')

    settings['template_env'] = env

    settings['contexts'] = {'channel': Channel}

    app = web.Application(handlers(static_path=static_path),
                          **settings)
    return app
