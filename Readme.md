django-featured-item
====================

Set up a model so that only one record can be featured at a time.

Think of the featured story on a news site. Only one article may be featured
at a time. Similar to this, only one record have have a featured field be true
at a time.

Models can have more than one featured field. Only one record can hold the
featured spot per field.

Setup
-----

1. Add `featured_item` to your `INSTALLED_APPS`:

	INSTALLED_APPS += (
		'featured_item',
	)

Usage
-----

Add a `FeaturedField` to your model:

	from django.db import models
	from featured_item.fields import FeaturedField

	class Story(models.Model):
		title = models.CharField(max_length=255)
		body = models.TextField()

		featured = FeaturedField()

That is it! Now, only one record in model can have `featured = True`.

You can have multiple `FeaturedField`s per model:

	class Story(models.Model):
		title = models.CharField(max_length=255)
		body = models.TextField()

		home_page_feature = FeaturedField()
		side_bar_feature = FeaturedField()
