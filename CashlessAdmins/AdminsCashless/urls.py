from django.urls import path
from . views import PaymentUpdateView
urlpatterns = [
      path('payment_update/',PaymentUpdateView.as_view(),name='payment_update'),
]
