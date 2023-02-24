from django.conf import settings
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin


class UserLocaleMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """Activate logged-in users' preferred language based on their profile setting."""
        user = getattr(request, "user", None)
        if not (user and user.is_authenticated):
            return

        if user.language and user.language != translation.get_language():
            translation.activate(user.language)

    def process_response(self, request, response):
        cookie_lang_code = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        if not cookie_lang_code or cookie_lang_code != translation.get_language():
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, translation.get_language())
        return response
