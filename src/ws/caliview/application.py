import pyramid_jinja2
import pyramid.config


class Application:
    def __call__(self, global_conf, **conf):
        self.configure_pyramid(conf)
        return self.config.make_wsgi_app()

    def configure_pyramid(self, conf):
        c = self.config = pyramid.config.Configurator()
        c.registry.settings.update(**conf)
        self.configure_jinja()

        c.add_route('home', '/')
        c.add_static_view('static', 'ws.caliview:static')
        c.scan(package=__package__)

    def configure_jinja(self):
        c = self.config
        c.add_directive(
            'add_jinja2_renderer', pyramid_jinja2.add_jinja2_renderer)
        c.add_directive(
            'add_jinja2_search_path', pyramid_jinja2.add_jinja2_search_path)
        c.add_directive(
            'add_jinja2_extension', pyramid_jinja2.add_jinja2_extension)
        c.add_directive(
            'get_jinja2_environment', pyramid_jinja2.get_jinja2_environment)

        c.add_jinja2_renderer('.html')
        c.add_jinja2_search_path('ws.caliview:', '.html')


app_factory = Application()
