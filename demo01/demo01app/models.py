from django.db import models
from django.conf import settings

# Create your models here.


class OwnedModel(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        abstract = True


# Transaction


class Transaction(OwnedModel):
    id = models.CharField('Id', primary_key=True, max_length=14, blank=False)
    paid = models.IntegerField('Paid', null=False)
    date = models.DateField('Date', null=False)
    product = models.CharField('Product', max_length=64, null=False)
