from rest_framework import serializers
from .models import CardHolder,Merchant,Payment,Transaction

class CardHolderSerializer(serializers.ModelSerializer):
	class Meta:
		model = CardHolder
		fields = ('card_id','qr_code','alias','balance')


class MerchantSerializer(serializers.ModelSerializer):
	class Meta:
		model = Merchant
		fields = ('wallet_id','balance','alias')

class PaymentSerializer(serializers.ModelSerializer):
	card_info = serializers.UUIDField(required=True)

	class Meta:
		model = Payment
		fields = ('amount','card_info','wallet_id')

class TransactionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Transaction
		fields = '__all__'
