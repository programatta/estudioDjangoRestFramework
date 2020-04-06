from django.db import models

# Create your models here.


class Transaction(models.Model):
    id = models.CharField('Id', primary_key=True, max_length=14, blank=False)
    paid = models.IntegerField('Paid', null=False)
    date = models.DateField('Date', null=False)
    product = models.CharField('Product', max_length=64, null=False)
    ownerId = models.CharField('OwnerId', max_length=46, null=False)

    objects = models.Manager()
