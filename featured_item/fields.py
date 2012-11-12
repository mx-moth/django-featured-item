from django.db import models
from django.db.models.signals import post_save


class FeaturedField(models.BooleanField):

    def __init__(self, *args, **kwargs):
        super(FeaturedField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(FeaturedField, self).contribute_to_class(cls, name)
        setattr(cls, self.name, self)
        post_save.connect(self.update_on_save, sender=cls)

    def __get__(self, instance, owner):
        if instance is None:
            raise AttributeError(
                "%s must be accessed via instance." % self.name)

        try:
            current, updated = getattr(instance, self.get_cache_name())
        except AttributeError:
            return self.default

        return current if updated is None else updated

    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError(
                "%s must be accessed via instance." % self.name)

        if value is None:
            value = self.default
        cache_name = self.get_cache_name()
        try:
            old, new = getattr(instance, cache_name)
        except AttributeError:
            old, new = value, None
        else:
            new = value

        setattr(instance, cache_name, (old, new))

    def pre_save(self, instance, add):
        cache_name = self.get_cache_name()
        old, new = getattr(instance, cache_name)

        if add:
            old = None
        else:
            old_instance = type(instance)._default_manager.get(pk=instance.pk)
            old = getattr(old_instance, self.name)

        if old is not None and new is None:
            return old

        setattr(instance, cache_name, (old, new))
        return new

    def update_on_save(self, sender, instance, created, **kwargs):

        cache_name = self.get_cache_name()
        try:
            old_value, new_value = getattr(instance, cache_name)
        except:
            old_value, new_value = None, getattr(instance, self.name)

        need_updating = new_value is True and old_value is not True

        # Quit early if nothing changed
        if not need_updating:
            return

        Model = type(instance)
        qs = Model._default_manager
        qs = qs.exclude(pk=instance.pk).filter(**{self.name: True})

        qs.update(**{self.name: False})

        setattr(instance, cache_name, (new_value, new_value))
