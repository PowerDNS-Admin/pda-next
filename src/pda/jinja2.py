from django.templatetags.static import static
from django.urls import reverse
from django.utils import translation
from inspect import getmembers, isfunction
from jinja2 import Environment
from lib.jinja import filters, tests


class JinjaEnvironment(Environment):

    def __init__(self, **kwargs):
        super(JinjaEnvironment, self).__init__(**kwargs)

        self.add_extension('jinja2.ext.i18n')

        self.install_gettext_translations(translation, newstyle=True)

        # Load filter definitions
        for item in getmembers(filters):
            if not str(item[0]).startswith('_') and isfunction(item[1]):
                self.filters[item[0]] = item[1]

        # Load test definitions
        for item in getmembers(tests):
            if not str(item[0]).startswith('_') and isfunction(item[1]):
                self.tests[item[0]] = item[1]

        self.globals.update({
            'static': static,
            'url': reverse,
        })
