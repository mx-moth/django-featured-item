from django.db import models
from django.test import TestCase

from featured_item.fields import FeaturedField


class SingleFeature(models.Model):
    name = models.CharField(max_length=255)
    featured = FeaturedField(default=False)


class MultipleFeature(models.Model):
    name = models.CharField(max_length=255)

    featured_1 = FeaturedField()
    featured_2 = FeaturedField()
    featured_3 = FeaturedField()


class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books')
    genre = models.CharField(max_length=255)
    featured = FeaturedField(unique_on=('author',))
    featured_in_genre = FeaturedField(unique_on=('author', 'genre'))


class FeaturedField(TestCase):

    def test_featured_item(self):

        a = SingleFeature.objects.create(name="a", featured=False)
        b = SingleFeature.objects.create(name="b", featured=False)
        c = SingleFeature.objects.create(name="c", featured=False)

        self.assertEqual(
            SingleFeature.objects.filter(featured=True).count(), 0,
            "No item is featured by default")

        a.featured = True
        a.save()

        self.assertEqual(
            SingleFeature.objects.get(featured=True).name, 'a',
            "Can set featured=True")

        b.featured = True
        b.save()

        self.assertEqual(
            SingleFeature.objects.filter(featured=True).count(), 1,
            "Only one featured item at a time")

        self.assertEqual(
            SingleFeature.objects.get(featured=True).name, 'b',
            "Featured item is now 'b'")

    def test_multiple_featured_fields(self):

        a = MultipleFeature.objects.create(name='a')
        b = MultipleFeature.objects.create(name='b')
        c = MultipleFeature.objects.create(name='c')

        a.featured_1 = True
        a.save()

        b.featured_2 = True
        b.save()

        c.featured_3 = True
        c.save()

        self.assertEqual(
            MultipleFeature.objects.get(featured_1=True).name, 'a',
            "Can set feature_1 correctly")

        self.assertEqual(
            MultipleFeature.objects.get(featured_2=True).name, 'b',
            "Can set feature_2 correctly")

        self.assertEqual(
            MultipleFeature.objects.get(featured_3=True).name, 'c',
            "Can set feature_3 correctly")

        # Get new instances, and update them
        a = MultipleFeature.objects.get(name='a')
        a.featured_3 = True
        a.save()

        c = MultipleFeature.objects.get(name='c')
        c.featured_2 = True
        c.save()

        # Things just changed back there, so get new instances again
        a = MultipleFeature.objects.get(name='a')
        c = MultipleFeature.objects.get(name='c')

        self.assertTrue(a.featured_1, "'a' is still feature 1")
        self.assertTrue(a.featured_3, "'a' is now feature 3")
        self.assertTrue(c.featured_2, "'c' is now feature 2")
        self.assertTrue(not c.featured_3, "'c' is no longer feature 3")

    def test_unique_on(self):

        meiville = Author.objects.create(name='China Mieville')
        banks = Author.objects.create(name='Iain Banks')

        m1 = meiville.books.create(name="Kraken", genre="Fantasy")
        m2 = meiville.books.create(name="Railsea", genre="Fantasy")
        m3 = meiville.books.create(name="The City & the City", genre="Crime")
        m4 = meiville.books.create(name="Embassytown", genre="Sci Fi")

        # To be pedantic, his Sci Fi works are published under  Iain M. Banks
        b1 = banks.books.create(name="The Business", genre="Fantasy")
        b2 = banks.books.create(name="Dead Air", genre="Fantasy")
        b3 = banks.books.create(name="Stonemouth", genre="Fantasy")
        b4 = banks.books.create(name="Matter", genre="Sci Fi")
        b5 = banks.books.create(name="The Algebraist", genre="Sci Fi")

        m1.featured = True
        m1.featured_in_genre = True
        m1.save()

        m4.featured_in_genre = True
        m4.save()

        b1.featured_in_genre = True
        b1.save()

        b5.featured = True
        b5.featured_in_genre = True
        b5.save()

        self.assertEqual(
            Book.objects.filter(featured_in_genre=True).count(), 4,
            "Four books are featured in their respective author/genre set")

        self.assertEqual(
            Book.objects.filter(featured=True).count(), 2,
            "Two books are featured in their respective author set")

        # Actually, Embassytown kicked arse!
        m4.featured = True
        m4.save()

        self.assertEqual(
            Book.objects.filter(featured_in_genre=True).count(), 4,
            "Four books are featured in their respective author/genre set")

        self.assertEqual(
            Book.objects.filter(featured=True).count(), 2,
            "Two books are featured in their respective author set")

        meivilles_best_book = Book.objects.get(
            author=meiville, featured=True)
        self.assertEqual(meivilles_best_book, m4,
            "Can update featured item with unique_to")

        banks_best_book = Book.objects.get(
            author=banks, featured=True)
        self.assertEqual(banks_best_book, b5,
            "Can update featured item with unique_to without changing others")

        banks_best_sci_fi = Book.objects.get(
            author=banks, genre="Sci Fi", featured_in_genre=True)
        self.assertEqual(banks_best_book, b5,
            "Other featured fields are not affected")

        b4.featured_in_genre = True
        b4.save()

        banks_best_sci_fi = Book.objects.get(
            author=banks, genre="Sci Fi", featured_in_genre=True)
        self.assertEqual(banks_best_sci_fi, b4,
            "Can change complex unique_to properly")
