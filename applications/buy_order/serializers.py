from rest_framework import serializers
from .models import BuyOrder


class BuyOrderSerializer(serializers.ModelSerializer):
    items = serializers.StringRelatedField(many=True)

    class Meta:
        model = BuyOrder
        fields = '__all__'
