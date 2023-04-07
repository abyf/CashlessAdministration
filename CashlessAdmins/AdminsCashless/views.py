from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CardHolder, Merchant, Manager, Payment
from .webhook import PaymentSerializer
from django.db.models import F
from decimal import Decimal

class PaymentUpdateView(APIView):
    def post(self,request):
        #Deserialize the payment payload
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_data = serializer.validated_data

        try:
            if 'card_id' in payment_data:
                cardholder = CardHolder.objects.select_for_update().get(card_id=payment_data['card_id'])
            elif 'qr_code' in payment_data:
                cardholder = CardHolder.objects.select_for_update().get(qr_code=payment_data['qr_code'])
            cardholder.balance = F('balance') - Decimal(payment_data['amount']) - (Decimal(payment_data['amount'])*0.01)
            cardholder,save()
        except CardHolder.DoesNotExist:
            return Response({'error':'Invalid cardholder'},status=400)

        try:
            merchant = Merchant.objects.select_for_update().get(wallet_id=payment_data['wallet_id'])
            merchant.balance = F('balance') + Decimal(payment_data['amount'])
            merchant.save()
        except Merchant.DoesNotExist:
            return Response({'error':'Invalid Merchant'},status=400)

        try:
            manager = Manager.objects.get(username='zgame')
            manager.balance = F('balance') + (Decimal(payment_data['amount'])*0.01)
            manager.cardholder_commission = F('cardholder_commission') + (Decimal(payment_data['amount'])*0.01)
            manager.save()
        except Manager.DoesNotExist:
            return Response({'error':'Manager not Found'},status=400)

        Payment.objects.create(cardholder=cardholder, merchant=merchant, commission_fee=payment_data['commission_fee'])

        return Response({'success':True})


def home(request):
    return render(request,'authenticate/home.html',{})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request,('Welcome {user}'))
            return redirect('home')
        else:
            return redirect('login')
    else:
        messages.success(request,('Failed to Log in: Unknown user/wrong credential!!!'))
        return render(request,'authenticate/login.html',{})
