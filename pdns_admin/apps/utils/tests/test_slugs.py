from django.test import SimpleTestCase

from ..slug import get_next_slug


class NextSlugTest(SimpleTestCase):
    def test_next_slug_basic(self):
        self.assertEqual("slug-11", get_next_slug("slug", 11))

    def test_next_slug_truncate(self):
        self.assertEqual("slug-11", get_next_slug("slug", 11, max_length=7))
        self.assertEqual("slu-11", get_next_slug("slug", 11, max_length=6))
        self.assertEqual("slu-100", get_next_slug("slug", 100, max_length=7))
        self.assertEqual("sl-100", get_next_slug("slug", 100, max_length=6))

    def test_next_slug_fail(self):
        with self.assertRaises(ValueError):
            get_next_slug("slug", 11111, max_length=6)
