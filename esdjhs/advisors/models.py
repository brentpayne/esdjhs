from django.db import models

# Create your models here.

class Company(models.Model):
    company_name = models.CharField(max_length=256)
    full_address = models.CharField(max_length=256)


class Advisor(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    crd = models.IntegerField()
    company = models.ForeignKey(Company)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)
