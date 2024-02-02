from django.db import models


class Country(models.Model):
    code = models.CharField(max_length=2)
    name = models.CharField(max_length=50, null=True)


class Timezone(models.Model):
    name = models.CharField(max_length=50)
    offset = models.IntegerField()
    offset_dst = models.IntegerField()
