from django.db import models
from django.core.validators import URLValidator


class Page(models.Model):
    """
    Model representing the detailed information of a page.

    Basic information:
    - For tags <h_{i}>, the number is stored in the database.
    - Links from tags <a> are stored in the database as a string, as an example, 'http://google.com, http://yandex.ru'.

    Extra information:
    - URL of a page.
    - Information update time.
    """
    url = models.URLField(max_length=200, validators=[URLValidator])
    h1 = models.PositiveIntegerField()
    h2 = models.PositiveIntegerField()
    h3 = models.PositiveIntegerField()
    a = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
