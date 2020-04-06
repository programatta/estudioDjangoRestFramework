from demo02app.models import Transaction
from rest_framework import serializers


class TransactionSerializer(serializers.ModelSerializer):
    # ownerId = serializers.HiddenField(
    #     default=serializers.CurrentUserDefault()
    # )

    class Meta:
        model = Transaction
        fields = ['id', 'paid', 'date', 'product', 'ownerId']
