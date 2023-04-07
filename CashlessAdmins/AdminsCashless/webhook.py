from rest_framework import serializers
from .models import CardHolder,Merchant,Payment,Transaction

class CardHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardHolder
        fields = '__all__'

class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('card_id','qr_code','wallet_id','amount','commission_fee')

class WebhookSerializer(serializers.Serializer):
    merchant = MerchantSerializer()
    cardholder = CardHolderSerializer()
