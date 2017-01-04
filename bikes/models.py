from django.db import models


class Bike(models.Model):
    COLOR_OPTIONS = (('yellow', 'Yellow'), ('red', 'Red'), ('black', 'Black'))

    color = models.CharField(max_length=255, null=True, blank=True,
                             choices=COLOR_OPTIONS)
    size = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    last_used = models.DateTimeField(null=True, blank=True)
