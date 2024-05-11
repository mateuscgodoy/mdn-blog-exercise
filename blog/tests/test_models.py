from django.contrib.auth import get_user_model
from django.test import TestCase

# The user model used is the default implement by Django
User = get_user_model()

from blog.models import Author


class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username="testuser1", password="1X<ISRUkw+tuK")

    def test_bio_label(self):
        user = User.objects.get(username="testuser1")
        author = Author.objects.create(user=user, bio="Some standard bio.")
        bio_label = author._meta.get_field("bio").verbose_name
        self.assertEqual(bio_label, "Biography")

    def test_bio_max_length(self):
        user = User.objects.get(username="testuser1")
        author = Author.objects.create(user=user, bio="Some standard bio.")
        max_length = author._meta.get_field("bio").max_length
        self.assertEqual(max_length, 1000)

    def test_bio_help_text(self):
        user = User.objects.get(username="testuser1")
        author = Author.objects.create(user=user, bio="Some standard bio.")
        help_text = author._meta.get_field("bio").help_text
        self.assertEqual(
            help_text, "Enter some information about yourself and your background."
        )

    def test_bio_default_value_is_expected(self):
        user = User.objects.get(username="testuser1")
        author = Author.objects.create(user=user)
        default = author._meta.get_field("bio").default
        self.assertEqual(default, "Author has not set any bio information yet.")

    def test_writes_since_label(self):
        user = User.objects.get(username="testuser1")
        author = Author.objects.create(user=user)
        writes_since_label = author._meta.get_field("writes_since").verbose_name
        self.assertEqual(writes_since_label, "writes since")

    def test_author_as_string(self):
        user = User.objects.get(username="testuser1")
        author = Author.objects.create(user=user)
        expected = str(author.user)
        self.assertEqual(str(author), expected)
