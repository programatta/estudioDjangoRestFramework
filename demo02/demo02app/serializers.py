from demo02app.models import Transaction
from rest_framework import serializers
from .aws.serializers.awsserializers import AWSDefaultFieldCurrentUser


class TransactionSerializer(serializers.ModelSerializer):
    ownerId = serializers.HiddenField(
        default=AWSDefaultFieldCurrentUser()
    )

    class Meta:
        model = Transaction
        fields = ['id', 'paid', 'date', 'product', 'ownerId']
