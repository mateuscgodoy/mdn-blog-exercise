import datetime
import pytz

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.db.utils import IntegrityError

# The user model used is the default implement by Django
User = get_user_model()

from blog.models import Author, Blog


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

    def test_can_not_create_author_without_user(self):
        with self.assertRaises(expected_exception=IntegrityError):
            Author.objects.create()

    def test_author_as_string(self):
        user = User.objects.get(username="testuser1")
        author = Author.objects.create(user=user)
        expected = str(author.user)
        self.assertEqual(str(author), expected)


class BlogModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="testuser1", password="1X<ISRUkw+tuK")
        Author.objects.create(user=user)

    def test_id_help_text(self):
        author = Author.objects.first()
        blog = Blog.objects.create(author=author)
        help_text = blog._meta.get_field("id").help_text
        self.assertEqual(help_text, "Unique ID representing this specific blog post")

    def test_title_maximum_characters(self):
        author = Author.objects.first()
        blog = Blog.objects.create(author=author)
        max_length = blog._meta.get_field("title").max_length
        self.assertEqual(max_length, 200)

    def test_created_at_title(self):
        author = Author.objects.first()
        blog = Blog.objects.create(author=author)
        created_at_label = blog._meta.get_field("created_at").verbose_name
        self.assertEqual(created_at_label, "created at")

    def test_ordering_is_ascending(self):
        author = Author.objects.first()
        Blog.objects.create(author=author)
        latest_blog = Blog.objects.create(author=author)

        first_blog = Blog.objects.all()[0]
        self.assertEqual(first_blog.created_at, latest_blog.created_at)

    def test_blog_as_string(self):
        author = Author.objects.first()
        title = "A nice blog"
        blog = Blog.objects.create(title=title, author=author)
        expected = f"{title} - {blog.created_at}"
        self.assertEqual(str(blog), expected)

    def test_raises_when_blog_has_no_author(self):
        with self.assertRaises(expected_exception=IntegrityError):
            Blog.objects.create()
